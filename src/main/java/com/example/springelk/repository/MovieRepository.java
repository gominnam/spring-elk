package com.example.springelk.repository;

import com.example.springelk.model.Movie;
import org.springframework.data.elasticsearch.annotations.Query;
import org.springframework.data.elasticsearch.repository.ElasticsearchRepository;

import java.util.List;

public interface MovieRepository extends ElasticsearchRepository<Movie, String> {
    Iterable<Movie> findByTitle(String title);

    @Query("{\"multi_match\": {\"query\": \"?0\", \"fields\": [\"title\", \"director\", \"genre\", \"cast\"]}}")
    List<Movie> searchByMultiMatch(String query);

}
