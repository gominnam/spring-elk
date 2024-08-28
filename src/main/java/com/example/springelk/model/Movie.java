package com.example.springelk.model;

import org.springframework.data.annotation.Id;
import org.springframework.data.elasticsearch.annotations.Document;

@Document(indexName = "wiki_movies")
@lombok.Data
public class Movie {
    @Id
    private String id;
    private int releaseYear;
    private String title;
    private String originEthnicity;
    private String director;
    private String cast;
    private String genre;
    private String wikiPage;
    private String plot;
}
