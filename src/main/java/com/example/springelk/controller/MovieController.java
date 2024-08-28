package com.example.springelk.controller;

import com.example.springelk.model.Movie;
import com.example.springelk.service.MovieService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;


@RestController
@RequestMapping("/movies")
public class MovieController {

    @Autowired
    private MovieService movieService;

    @GetMapping("/search")
    public Iterable<Movie> search(@RequestParam("title") String title) {
        return movieService.findByTitle(title);
    }
}
