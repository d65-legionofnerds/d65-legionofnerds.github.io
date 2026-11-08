# Builds the list of stories that the homepage, section pages, All stories and the side rails read,
# and checks every page's front matter so a mistake stops the build with a plain message instead of
# a page quietly missing from the homepage.
#
# A "story" is any page whose front matter has `topic:`, plus every entry in _data/links.yml.
# Templates read:
#   site.data.stories      every story, newest first
#   site.data.lead_story   the story that leads the homepage
#   page.related           up to 3 newer-first stories from the same topic (article pages)
#   page.type_label, page.topic_name, page.read_minutes, page.description
require "date"

module LDN
  class Stories < Jekyll::Generator
    safe true
    priority :highest

    WORDS_PER_MINUTE = 230
    MAX_MARKS = 3

    def generate(site)
      @site = site
      @errors = []
      @warnings = []
      topics = (site.data["topics"] || []).to_h { |t| [t["id"], t] }
      types = (site.data["types"] || []).to_h { |t| [t["id"], t] }

      stories = []

      site.pages.each do |page|
        next unless page.data.key?("topic")
        where = page.relative_path
        d = page.data
        check_fields(where, d, topics, types)
        date = to_date(where, "date", d["date"])
        updated = d["updated"] ? to_date(where, "updated", d["updated"]) : nil
        next unless date

        if d["image"]
          img = d["image"].to_s.sub(%r{\A/}, "")
          @errors << "#{where}: image #{d['image']} doesn't exist." unless File.exist?(File.join(site.source, img))
          @warnings << "#{where}: has an image but no image_alt (describe the chart for screen readers)." unless d["image_alt"]
        elsif d["type"] == "analysis"
          @warnings << "#{where}: analysis has no `image:`. It will lead the homepage without a picture and link previews will show the logo. Make one with tools/chart_image.py."
        end

        marks = page.content.to_s.scan(/<mark[\s>]/).size
        @warnings << "#{where}: #{marks} highlights. House style is one or two per piece." if marks > MAX_MARKS
        if d["takeaways"] && !d["takeaways"].is_a?(Array)
          @errors << "#{where}: takeaways must be a list (each line starting with '- ')."
        end

        minutes = [(word_count(page.content.to_s) / WORDS_PER_MINUTE.to_f).round, 1].max
        topic = topics[d["topic"]] || {}
        type = types[d["type"]] || {}
        d["read_minutes"] = minutes
        d["type_label"] = type["label"]
        d["topic_name"] = topic["name"]
        d["topic_short"] = topic["short"]
        d["description"] ||= plain(d["summary"])

        stories << story_hash(d, date, updated, topic, type, page.url, false).merge("minutes" => minutes, "path" => page.relative_path)
      end

      (site.data["links"] || []).each_with_index do |d, i|
        where = "_data/links.yml entry #{i + 1} (#{d['title'] || 'no title'})"
        check_fields(where, d, topics, types)
        @errors << "#{where}: needs a `link:`." unless d["link"]
        date = to_date(where, "date", d["date"])
        updated = d["updated"] ? to_date(where, "updated", d["updated"]) : nil
        next unless date && d["link"]
        link = d["link"].to_s
        external = link.match?(%r{\Ahttps?://})
        unless external
          @errors << "#{where}: link #{link} doesn't exist in the repo." unless File.exist?(File.join(site.source, link.sub(%r{\A/}, "")))
          link = "/" + link.sub(%r{\A/}, "")
        end
        stories << story_hash(d, date, updated, topics[d["topic"]] || {}, types[d["type"]] || {}, link, external).merge("path" => "_data/links.yml")
      end

      stories.sort_by! { |s| [-s["date"].jd, s["title"].to_s] }
      site.data["stories"] = stories

      pinned = stories.select { |s| s["lead"] && s["type"] == "analysis" }
      site.data["lead_story"] = pinned.first || stories.find { |s| s["type"] == "analysis" && !s["external"] }

      # Related stories for article pages: same topic, newest first, not itself.
      site.pages.each do |page|
        next unless page.data.key?("topic")
        page.data["related"] = stories.select { |s| s["topic"] == page.data["topic"] && s["url"] != page.url }.first(3)
      end

      # Resolve the source page of each "By the numbers" figure to its URL.
      (site.data["numbers"] || []).each do |n|
        src = site.pages.find { |p| p.relative_path == n["source"].to_s.sub(%r{\A/}, "") }
        if src
          n["url"] = src.url
        else
          @errors << "_data/numbers.yml: #{n['value']} cites #{n['source']}, which isn't a page on the site."
        end
      end

      @warnings.each { |w| Jekyll.logger.warn "Check:", w }
      return if @errors.empty?

      msg = "The site didn't build because of #{@errors.size} problem(s) with page settings:\n  - " +
            @errors.join("\n  - ") +
            "\nFix these in the files named above (see CLAUDE.md, 'Front matter'), then push again."
      raise Jekyll::Errors::FatalException, msg
    end

    private

    def check_fields(where, d, topics, types)
      %w[title date topic type summary].each do |k|
        @errors << "#{where}: missing `#{k}:`." if d[k].nil? || d[k].to_s.strip.empty?
      end
      if d["topic"] && !topics.key?(d["topic"])
        @errors << "#{where}: topic `#{d['topic']}` isn't one of: #{topics.keys.join(', ')} (see _data/topics.yml)."
      end
      if d["type"] && !types.key?(d["type"])
        @errors << "#{where}: type `#{d['type']}` isn't one of: #{types.keys.join(', ')} (see _data/types.yml)."
      end
      if d["summary"] && plain(d["summary"]).length > 320
        @warnings << "#{where}: summary is #{plain(d['summary']).length} characters. Keep it to one or two sentences (under about 250)."
      end
    end

    def story_hash(d, date, updated, topic, type, url, external)
      {
        "title" => d["title"],
        "url" => url,
        "external" => external,
        "date" => date,
        "updated" => updated,
        "month" => date.strftime("%Y-%m"),
        "month_label" => date.strftime("%B %Y"),
        "topic" => d["topic"],
        "topic_name" => topic["name"],
        "topic_short" => topic["short"],
        "type" => d["type"],
        "type_label" => type["label"],
        "type_group" => type["group"],
        "format" => d["format"],
        "summary" => d["summary"],
        "image" => d["image"],
        "image_alt" => d["image_alt"],
        "image_caption" => d["image_caption"],
        "featured" => d["featured"] ? true : false,
        "lead" => d["lead"] ? true : false
      }
    end

    def to_date(where, key, v)
      case v
      when Date then v.is_a?(DateTime) ? v.to_date : v
      when Time then v.to_date
      when String
        begin
          Date.parse(v)
        rescue ArgumentError
          @errors << "#{where}: #{key} `#{v}` isn't a date. Write it as YYYY-MM-DD." ; nil
        end
      when nil then nil
      else
        @errors << "#{where}: #{key} `#{v}` isn't a date. Write it as YYYY-MM-DD." ; nil
      end
    end

    def plain(s)
      s.to_s.gsub(/<[^>]+>/, "").gsub(/\s+/, " ").strip
    end

    def word_count(text)
      t = text.gsub(/\{%.*?%\}|\{\{.*?\}\}/m, " ")
              .gsub(/<(script|style)\b.*?<\/\1>/mi, " ")
              .gsub(/<[^>]+>/, " ")
              .gsub(/\|/, " ")
      t.scan(/[[:alnum:]][[:alnum:]'’\-.,%$]*/).size
    end
  end
end
