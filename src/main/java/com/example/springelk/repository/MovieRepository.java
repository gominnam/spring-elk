package com.example.springelk.repository;

import com.example.springelk.model.Movie;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.elasticsearch.annotations.Query;
import org.springframework.data.elasticsearch.repository.ElasticsearchRepository;

import java.util.List;

public interface MovieRepository extends ElasticsearchRepository<Movie, String> {
    Iterable<Movie> findByTitle(String title);

    @Query("{\"multi_match\": {\"query\": \"?0\", \"fields\": [\"title\", \"director\", \"genre\", \"cast\"]}}")
    List<Movie> searchByMultiMatch(String query);

    @Query("{\"term\": {\"poster_image_url.keyword\": \"null\"}}")
    Page<Movie> findByPosterImageUrlIsNull(Pageable pageable);

    @Query("{\"script\": {\"inline\": \"ctx._source.posterImageUrl = params.posterImageUrl\", \"params\": {\"posterImageUrl\": \"?0\"}}, \"query\": {\"term\": {\"_id\": \"?1\"}}}")
    void updatePosterImageUrl(String posterImageUrl, String id);
}
