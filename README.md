


### csv file edit special characters 

```
# prompt: read csv named "input.csv", remove 3 special characters (newline, double quote, comma) within any data, and export to "output.csv"

from tqdm import tqdm
import csv
with open('wiki_movie_plots_deduped.csv', 'r') as infile, open('output.csv', 'w') as outfile:
  reader = csv.reader(infile)
  writer = csv.writer(outfile)
  for row in tqdm(reader):
    new_row = [''.join(c for c in s if c not in ['\n']) for s in row]
    writer.writerow(new_row)
    
```

## References

- [Kaggle Dataset](https://www.kaggle.com/datasets/jrobischon/wikipedia-movie-plots)
- [Elasticsearch Srping](https://docs.spring.io/spring-data/elasticsearch/reference/elasticsearch/clients.html)