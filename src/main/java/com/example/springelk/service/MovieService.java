package com.example.springelk.service;

import com.example.springelk.model.Movie;
import com.example.springelk.repository.MovieRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

@Service
public class MovieService {
    @Autowired
    private MovieRepository movieRepository;

    public Iterable<Movie> findByTitle(String title) {
        return movieRepository.findByTitle(title);
    }
}
