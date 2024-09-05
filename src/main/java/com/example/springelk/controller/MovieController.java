package com.example.springelk.controller;

import com.example.springelk.model.Movie;
import com.example.springelk.service.MovieService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import java.io.IOException;
import java.util.List;


@RestController
@RequestMapping("/movies")
public class MovieController {

    @Autowired
    private MovieService movieService;

    @GetMapping("/title")
    public Iterable<Movie> getMovieByTitle(@RequestParam("title") String title) {
        return movieService.findByTitle(title);
    }

    @GetMapping("/multi-match-search")
    public List<Movie> searchByMultiMatch(@RequestParam("query") String query) {
        return movieService.searchByMultiMatch(query);
    }

    @PostMapping("/update-poster-images")
    public void updatePosterImages() throws IOException {
        movieService.updatePosterImageUrls();
    }

//    @PostMapping("/update-poster-images")
//    public void updatePosterImages(@RequestParam("batchSize") int batchSize) throws IOException {
//        movieService.updatePosterImageUrls(batchSize);
//    }
}
