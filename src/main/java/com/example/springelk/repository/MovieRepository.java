package com.example.springelk.repository;

import com.example.springelk.model.Movie;
import org.springframework.data.elasticsearch.repository.ElasticsearchRepository;

public interface MovieRepository extends ElasticsearchRepository<Movie, String> {
    Iterable<Movie> findByTitle(String title);
}
