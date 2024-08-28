package com.example.springelk.repository;

import com.example.springelk.model.Movie;
import org.springframework.data.elasticsearch.repository.ElasticsearchRepository;

import java.util.List;

public interface MovieRepository extends ElasticsearchRepository<Movie, String> {
    Iterable<Movie> findByTitle(String title);
    List<Movie> findByTitleContaining(String title);
//    List<Movie> findByGenreContaining(String genre);
//    List<Movie> findByCastContaining(String cast);
}
