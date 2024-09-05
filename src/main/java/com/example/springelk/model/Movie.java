package com.example.springelk.model;

import org.springframework.data.annotation.Id;
import org.springframework.data.elasticsearch.annotations.Document;
import org.springframework.data.elasticsearch.annotations.Field;
import org.springframework.data.elasticsearch.annotations.FieldType;

@Document(indexName = "wiki_movies")
@lombok.Data
public class Movie {
    @Id
    private String id;
    @Field(name = "release_year", type = FieldType.Integer)
    private int releaseYear;
    private String title;
    private String origin;
    private String director;
    private String cast;
    private String genre;
    @Field(name = "wiki_page", type = FieldType.Text)
    private String wikiPage;
    private String plot;

    @Field(name = "poster_image_url", type = FieldType.Text)
    private String posterImageUrl;
}
