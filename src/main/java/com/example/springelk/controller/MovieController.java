package com.example.springelk.controller;

import com.example.springelk.model.Movie;
import com.example.springelk.service.MovieService;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.servlet.ModelAndView;

import java.io.IOException;
import java.util.List;


@RestController
@RequestMapping("/movies")
public class MovieController {

    @Autowired
    private MovieService movieService;

    static final Logger log = LoggerFactory.getLogger(MovieController.class);

    @GetMapping("/title")
    public Iterable<Movie> getMovieByTitle(@RequestParam("title") String title) {
        return movieService.findByTitle(title);
    }

    @GetMapping("/multi-match-search")
    public ModelAndView searchByMultiMatch(@RequestParam("query") String query, Model model) {
        List<Movie> movies = movieService.searchByMultiMatch(query);
        model.addAttribute("movies", movies);

        // Log each movie's data
        for (Movie movie : movies) {
            log.info("Movie: {}", movie);
        }
        
        return new ModelAndView("home", "moviesModel", model);
    }

    @GetMapping("/multi-match-search-api")
    public List<Movie> searchByMultiMatch(@RequestParam("query") String query) {
        return movieService.searchByMultiMatch(query);
    }

    @PostMapping("/update-poster-images")
    public void updatePosterImages() throws IOException {
        movieService.updatePosterImageUrls();
    }
}
