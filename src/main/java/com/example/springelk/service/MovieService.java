package com.example.springelk.service;

import com.example.springelk.model.Movie;
import com.example.springelk.repository.MovieRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.ArrayList;
import java.util.HashSet;
import java.util.List;
import java.util.Set;

@Service
public class MovieService {
    @Autowired
    private MovieRepository movieRepository;

    public Iterable<Movie> findByTitle(String title) {
        return movieRepository.findByTitle(title);
    }

    public List<Movie> findByCriteria(String query) {
        List<Movie> moviesByTitle = movieRepository.findByTitleContaining(query);
//        List<Movie> moviesByGenre = movieRepository.findByGenreContaining(query);
//        List<Movie> moviesByCast = movieRepository.findByCastContaining(query);

        // Combine results, avoiding duplicates
        Set<Movie> combinedResults = new HashSet<>();
        combinedResults.addAll(moviesByTitle);
//        combinedResults.addAll(moviesByGenre);
//        combinedResults.addAll(moviesByCast);

        return new ArrayList<>(combinedResults);
    }
}
