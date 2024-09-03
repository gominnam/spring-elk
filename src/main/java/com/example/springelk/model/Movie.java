package com.example.springelk.model;

import org.springframework.data.annotation.Id;
import org.springframework.data.elasticsearch.annotations.Document;

@Document(indexName = "wiki_movies")
@lombok.Data
public class Movie {
    @Id
    private String id;
    private int release_year;
    private String title;
    private String origin;
    private String director;
    private String cast;
    private String genre;
    private String wiki_page;
    private String plot;
}
