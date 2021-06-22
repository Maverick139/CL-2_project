

# Hindi Text Summarizer
An extractive text summarizer with a tf-idf driven topic selection algorithm, controlled by compression extent specified by the user.

## Getting Started

### Dependecies
- Python 3.7

### How to use
The script takes a single input text file with individual sentences in Hindi unicode (utf-8) in each line, and the desired compression pecentage (stable compression range: 50% - 99%).

```
python3 hindi_summarizer.py <input_file_path.txt> <output_percentage>
```
Eg.
```
python3 hindi_summarizer.py sample_input_1.txt 75 # summary saved to output.txt
```

## Author

  **KV Aditya Srivatsa** (k.v.aditya@research.iiit.ac.in)
 
 If you have any queries, please do reach out. 

## License
Refer to the [LICENSE](https://github.com/kvadityasrivatsa/parsing-assisted-sentence-paraphrasing/blob/main/LICENSE) file for more details.

