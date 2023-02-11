# <center>How to create a wordlist for a given language</center>

## 1. Download a recent Wikipedia dump file for the given language.
  * From the [Wikimedia download directory](https://dumps.wikimedia.org/backup-index.html), select a Wikimedia download file for the given language.
  * **Note:** The term "article" denotes the encyclopedic entries. The term "page" broader, and includes other sources, such as talk pages, documentation, lists of recent changes, etc.
  * **Example:** For language Esperanto (which has code "eo"), one could choose the file <tt>eowiki-YYYYMMDD-pages-articles.xml.bz2</tt>.
  * **Note:** Uncompressing the file manually (e.g., <tt>bzip -d eowiki.YYYYMMDD-pages-articles.xml.bz2</tt>) is not needed. The next step takes care of uncompressing the file.

## 2. Extract text from the file.
  * One possible tool is [WikiExtractor.py](https://git/arpertium/WikiExtractor/WikiExtractor.py), in the github user apertium's WikiExtractor repo.
  * With this tool, the following command creates a file called <tt>wiki.txt</tt>.
    >  <tt>% python WikiExtractor.py --infn eowiki.YYYYMMDD-pages-articles.xml.bz2</tt>

## 3. Break file wiki.txt into lines and words:
  * Convert various word-adjacent characters to spaces: (),:;"'
  * Leave periods intact, to prevent treating second-level domain names as words, as in "foo.com" ==> "foo com".
  * Within each line, break on spaces. Keep only words consisting entirely letters, hyphens, and an optional final period.
    - Remove a final period, if there is one.
    - Remove words:
      - starting or ending with a hyphen
      - containing a double-hyphen
      - with no vowels

## 4. Merge in words from sources other than Wikipedia.
  * Read in wordlists from other sources, and merge into the wordlists already created. (Use sets to automatically de-dupe.)

## 5. Write wordlist file and install.
  * Write wordlist(s) to files (e.g., <tt>eo\_words.txt</tt> and <tt>eo\_caps.txt</tt>), and install to final location (e.g., <tt>/usr/share/dict/</tt>).
  * For Esperanto, the number of words in the output word file is about 9.5 times the number of lower-case words in the Linux English word file <tt>/usr/share/dict/words</tt>.

# Sources of errors
The following types of errors can find their way into the generated wordlists.

  * English and international words.
    - **Examples:** <tt>croc, webconferencing, welterweight, zydeco</tt>, etc.
  * Foreign words or phrases in pages on foreign languages, people, or places.
    - **Note:** These errors might be reduced if the Wikipedia extractor could be made to ignore text in italics.
  * Random other strings that might appear.
    - **Example:** A nucleotide sequence, such as <tt>atggccctgtggatgcgcctcctgccc</tt>.
  * Vandalism on Wikipedia pages. It happens.

> The rate of words not in the target language varies with the target language. For the case of Esperanto, above, it ended up being about 6%.

# TODO
## 1. Filter out English words that made their way into the other language's Wikipedia.
  * Filter out English words that leaked into the target language's wordlist.
  * But add back in words that are both English and the target language, possibly with different meanings. (Examples for English and Esperanto: <tt>ago, angle, cent, do, dura, en, filo, for, jam, kapo, nun, pro, tempo, urban, uzi</tt>.) Reviewing the intersection can be labor-intensive.
