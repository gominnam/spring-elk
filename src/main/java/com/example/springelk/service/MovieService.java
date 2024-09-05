package com.example.springelk.service;

import com.example.springelk.model.Movie;
import com.example.springelk.repository.MovieRepository;
import com.example.springelk.util.WikiCrawler;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.PageRequest;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.io.IOException;
import java.util.List;

@Service
public class MovieService {
    @Autowired
    private MovieRepository movieRepository;

    @Autowired
    private WikiCrawler wikiCrawler;

    static final Logger log = LoggerFactory.getLogger(MovieService.class);

    public Iterable<Movie> findByTitle(String title) {
        return movieRepository.findByTitle(title);
    }

    public List<Movie> searchByMultiMatch(String query) {
        return movieRepository.searchByMultiMatch(query);
    }

    @Transactional
    public void updatePosterImageUrls() throws IOException {
        int page = 0;
        int size = 5;
        Page<Movie> moviesPage;

        do {
            if(page > 2) break; // test code

            moviesPage = movieRepository.findByPosterImageUrlIsNull(PageRequest.of(page, size));
            List<Movie> movies = moviesPage.getContent();
            log.info("Query executed successfully, found {} movies", movies.size());

            for (Movie movie : movies) {
                log.info("Fetching poster image url for movie: " + movie.getTitle());
                String posterImageUrl = wikiCrawler.fetchPosterImageUrl(movie.getWikiPage());
                log.info("Updating poster image url for movie: " + posterImageUrl);
                 if (posterImageUrl != null) {
                     movieRepository.updatePosterImageUrl(posterImageUrl, movie.getId());
//                     movie.setPosterImageUrl(posterImageUrl);
//                     movieRepository.save(movie);
                 }
            }
            page++;
        } while (moviesPage.hasNext());
    }

}
