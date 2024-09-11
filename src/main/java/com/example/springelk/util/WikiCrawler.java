package com.example.springelk.util;

import org.jsoup.Jsoup;
import org.jsoup.nodes.Document;
import org.jsoup.nodes.Element;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.stereotype.Component;

import java.io.IOException;

@Component
public class WikiCrawler {

    final static Logger log = LoggerFactory.getLogger(WikiCrawler.class);

    public String fetchPosterImageUrl(String wikiPage) throws IOException {
        Document doc = Jsoup.connect(wikiPage).get();
        Element infoboxImage = doc.select(".infobox-image img").first();

        if (infoboxImage != null) {
            String posterUrl = "https:" + infoboxImage.attr("src");
            return posterUrl;
        } else {
            return null;
        }
    }
}
