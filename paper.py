from datetime import date
import urllib, json, sys, re
import xml.etree.ElementTree as ET
from os.path import exists as PathExists

reload(sys)
sys.setdefaultencoding('utf-8')

last_paper_id = 0
last_collection_id = 0
last_collection_order_num = 0

class Paper(object):
    """Represent an article(paper).

    Args:
        paper_id (:obj:`int`): `None` should be given for a new :class:`Paper` object. 
                               but it must be saved by calling :meth:`save_id_for_new()`
                               method after each new :class:`Paper` instance creation.

    Attributes:
        creation_date (obj:`str`): Date on which the paper object created.
        title (obj:`str`): Title of the article.
        author (obj:`str`): Name of authors, all in one string separated by commas.
        journal (obj:`str`): Name of the journal the article has been published.
        year (obj:`str`): Publication year of the article (e.g. '2017').
        volume (obj:`str`): Volume of the journal.
        issue (obj:`str`): Issue of the journal.
        pages (obj:`str`): Page numbers in one string (e.g. '137-145').
        doi (obj:`str`): DOI of article.
        url (obj:`str`): URL of article, mostly useful for arXiv links.
        comment (obj:`str`): User comment about the article.
        id (:obj:`int`): Id number of article(paper) instance.
        collection_id (obj:`str`): Id of the :class:`collection` object in which the 
                                   paper object belongs to.
    """

    def __init__(self, paper_id=None, creation_date='', title='', author='', journal='',
                    year='', volume='', issue='', pages='', doi='', url='', comment='', collection_id=None):
        self.creation_date = creation_date
        self.title = title
        self.author = author
        self.journal = journal
        self.year = year
        self.volume = volume
        self.issue = issue
        self.pages = pages
        self.doi = doi
        self.url = url
        self.comment = comment
        self.collection_id = collection_id
        if paper_id:
            self.id = paper_id
        else:
            self.id = None
            self.creation_date = date.today().strftime('%Y-%m-%d')

    def save_id_for_new(self):
        """Save an :attr:`Paper.id` for the new and empty :class:`paper` object."""
        if not self.id:
            global last_paper_id
            last_paper_id += 1
            self.id = last_paper_id
            return True
        else:
            return False

    def match(self, filter):
        """Check (case insensitively) whether the `filter` matches with
        some :class:`Paper` attributes or not.

        """

        filter = filter.lower()
        return filter in self.title.lower() \
            or filter in self.author.lower() \
            or filter in self.journal.lower() \
            or filter in self.year.lower() \
            or filter in self.volume.lower() \
            or filter in self.issue.lower() \
            or filter in self.pages.lower() \
            or filter in self.doi.lower() \
            or filter in self.url.lower() \
            or filter in self.comment.lower()




class Collection(object):
    """Represent a collection.
    
    Args:
        col_id (:obj:`int`): `None` should be given for a new :class:`Collection` object. 
                             but it must be saved by calling :meth:`save_id_for_new()` 
                             method after each new :class:`Collection` instance creation.

    Attributes:
        id (:obj:`int`): Id number of the collection object.
        name (obj:`str`): Name of collection.
        comment (obj:`str`): User comment for the collection.
        order_num (:obj:`int`): A unique number for each :class:`Collection` object
                                to be listed in an ascending order among other
                                :class:Collection instances.
        deleted (:obj:`int`): `0` if collection is not deleted, `1` otherwise.

    """

    def __init__(self, col_id=None, name='', comment='', order_num=None, deleted=0):
        self.id = col_id
        self.name = name
        self.comment = comment
        self.order_num = order_num
        self.deleted = deleted

    def save_id_for_new(self):
        """Save an attr:`Collection.id` for the new and empty :class:`Collection` object."""
        if not self.id:
            global last_collection_id
            global last_collection_order_num
            last_collection_id += 1
            last_collection_order_num += 1
            self.id = last_collection_id
            self.order_num = last_collection_order_num
            return True
        else:
            return False

    def match(self, filter):
        """Search (case insensitively) whether the `filter` matches with some 
        :class:`Collection` attributes or not.

        """

        filter == filter.lower()
        return filter in self.name.lower() \
            or filter in self.comment.lower() \
            or filter in str(self.order_num)

    


class CollectionHolder(object):
    """A holder for :class:`Collection` instances.

    Choose between `input` and `raw_input` for python 2.x and 3.x compatibility.
    Create an empty :obj:`list` object named :attr:`collections` lists :class:`Collection` 
    instances. If `./data/collections.json` path exists read the data from `json` file and load 
    :class:Collection instances to :attr:`collections` :obj:`list`.

    Attributes:
        collections (:obj:`list`): :obj:`list` of all :class:`Collection` instances.
        chosen_collection (:class:`Collection`): The instance of the chosen :class:`Collection`.

    """

    def __init__(self):
        global input
        global raw_input
        try: input = raw_input
        except NameError: pass
        self.collections = []
        max_id = 0
        max_order_num = 0
        if PathExists('./data/collections.json'):
            with open('./data/collections.json') as data_file:
                collections_list = json.load(data_file)
            for collection_dict in collections_list:
                if collection_dict['id'] > max_id: 
                    max_id = collection_dict['id']
                if collection_dict['order_num'] > max_order_num:
                    max_order_num = collection_dict['order_num']
                self.collections.append(Collection(collection_dict['id'],
                                                   collection_dict['name'],
                                                   collection_dict['comment'],
                                                   collection_dict['order_num'],
                                                   collection_dict['deleted']))
            data_file.close()
        global last_collection_id
        global last_collection_order_num
        last_collection_id = max_id
        last_collection_order_num = max_order_num
        self.chosen_collection = None
        self.sort()

    def choose_by_id(self, collection_id):
        """Choose a :class:`Collection` instance by its :attr:`Collection.id` attribute value."""
        for collection in self.collections:
            if collection.id == collection_id:
                self.chosen_collection = collection

    def new_collection(self):
        """Create a new :class:`Collection` instance."""
        self.chosen_collection = Collection()

    def add_name(self):
        """Add(overwrite) name to :attr:`Collection.name` attribute of chosen :class:`Collection`."""
        if self.chosen_collection:
            name = input("Enter name: ")
            self.chosen_collection.name = name
            self.save_collection()

    def add_comment(self):
        """Add(overwrite) comment to :attr:`Collection.comment` attribute of chosen :class:`Collection`."""
        if self.chosen_collection:
            comment = input("Enter comment: ")
            self.chosen_collection.comment = comment
            self.save_collection()

    def add_order_number(self):
        """Add(overwrite) ordering number to :attr:`Collection.order_number` attribute of chosen :class:`Collection`."""
        if self.chosen_collection:
            global last_collection_order_num
            print('Max Order number is: {0}'.format(last_collection_order_num))
            order_num = int(input("Enter order number: "))
            if order_num > last_collection_order_num:
                print('Order number cannot be greater than {0}'.format(last_collection_order_num))
            else:
                if order_num < self.chosen_collection.order_num:
                    self.chosen_collection.order_num = order_num
                    for collection in self.collections:
                        if order_num <= collection.order_num:
                            if self.chosen_collection.id != collection.id:
                                collection.order_num += 1
                elif order_num > self.chosen_collection.order_num:
                    self.chosen_collection.order_num = order_num
                    for collection in self.collections:
                        if order_num >= collection.order_num:
                            if self.chosen_collection.id != collection.id:
                                collection.order_num -= 1
            self.save_collection()

    def save_collection(self):
        """Save a unique id number if the object is a newly instantiated :class:`Collection` object.

        Then append this :class:`Collection` to :attr:`CollectionHolder.collections` :obj:`list`, update
        `json` data file by calling :meth:`CollectionHolder.save_json()` and at last uptade the order of 
        :class:`Collection` instances in :attr:`CollectionHolder.collections` :obj:`list` by calling 
        :meth:`CollectionHolder.sort()`.

        """

        if self.chosen_collection:
            if self.chosen_collection.save_id_for_new():
                self.collections.append(self.chosen_collection)
            self.save_json()
            self.sort()

    def sort(self):
        """Sort :attr:`collections` :obj:`list` by attr:`Collection.order_num` in ascending order."""
        self.collections = sorted(self.collections, key=lambda collection: collection.order_num)

    def delete(self):
        """Delete(hide) :class:`Collection` object.

        Delete by setting :attr:`Collection.deleted` value from `0` to `1`. :class:`Collection` 
        instance still will be in :attr:`CollectionHolder.collections` :obj:`list` and in json 
        data file, but will not appear in exported markdown pages.

        """

        if self.chosen_collection:
            self.chosen_collection.deleted = 1
            self.chosen_collection = None
            self.save_json()

    def save_json(self):
        """Save a `json` file holding all :class:`Collection` instance attributes in `json` data format."""
        if len(self.collections) > 0:
                with open('./data/collections.json', 'w') as output_file:
                    json.dump([collection.__dict__ for collection in self.collections], output_file)
                output_file.close


    def search_collections(self, filter):
        """Check if `filter` matches with some attributes of undeleted :class:`Collection` instances."""
        return [collection for collection in self.collections if
                collection.match(filter) and collection.deleted == 0]




class PaperMark(object):
    """ A holder for :class:Paper instances.

    Choose between `input` and `raw_input` for python 2.x and 3.x compatibility.
    Create an empty :obj:`list` object named :attr:`papers` lists :class:`Paper` 
    instances. If `./data/papers.json` path exists read the data from `json` file and load 
    :class:Paper instances to :attr:`papers` :obj:`list`.

    Attributes:
        papers (:obj:`list`): :obj:`list` of all :class:`Paper` instances.
        chosen_paper (:class:`Paper`): The instance of the chosen :class:`Paper`.

    """

    def __init__(self):
        global input
        global raw_input
        try: input = raw_input
        except NameError: pass
        self.papers = []
        max_id = 0
        if PathExists('./data/papers.json'):
            with open('./data/papers.json') as data_file:
                papers_list = json.load(data_file)
            for paper_dict in papers_list:
                if paper_dict['id'] > max_id: max_id = paper_dict['id']
                self.papers.append(Paper(paper_dict['id'], 
                                         paper_dict['creation_date'], 
                                         paper_dict['title'], 
                                         paper_dict['author'], 
                                         paper_dict['journal'],
                                         paper_dict['year'], 
                                         paper_dict['volume'], 
                                         paper_dict['issue'],
                                         paper_dict['pages'],
                                         paper_dict['doi'],
                                         paper_dict['url'],
                                         paper_dict['comment'],
                                         paper_dict['collection_id']))
            data_file.close()
        global last_paper_id
        last_paper_id = max_id
        self.chosen_paper = None
        self.sort()

    def choose_by_id(self, paper_id):
        """Choose a :class:`Paper` instance by its :attr:`Paper.id` attribute value."""
        for paper in self.papers:
            if paper.id == paper_id:
                self.chosen_paper = paper

    def new_paper(self):
        """Create a new :class:`Paper` instance."""
        self.chosen_paper = Paper()

    def add_title(self):
        """Add(overwrite) title to :attr:`Paper.title` attribute of chosen :class:`Paper`."""
        if self.chosen_paper:
            title = input("Enter title: ")
            self.chosen_paper.title = title
            self.save_paper()

    def add_author(self):
        """Add(overwrite) author to :attr:`Paper.author` attribute of chosen :class:`Paper`."""
        if self.chosen_paper:
            author = input("Enter author: ")
            self.chosen_paper.author = author
            self.save_paper()

    def add_journal(self):
        """Add(overwrite) journal to :attr:`Paper.journal` attribute of chosen :class:`Paper`."""
        if self.chosen_paper:
            journal = input("Enter journal: ")
            self.chosen_paper.journal = journal
            self.save_paper()

    def add_year(self):
        """Add(overwrite) year to :attr:`Paper.year` attribute of chosen :class:`Paper`."""
        if self.chosen_paper:
            year = input("Enter year: ")
            self.chosen_paper.year = year
            self.save_paper()

    def add_volume(self):
        """Add(overwrite) volume to :attr:`Paper.volume` attribute of chosen :class:`Paper`."""
        if self.chosen_paper:
            volume = input("Enter volume: ")
            self.chosen_paper.volume = volume
            self.save_paper()

    def add_issue(self):
        """Add(overwrite) issue to :attr:`Paper.issue` attribute of chosen :class:`Paper`."""
        if self.chosen_paper:
            issue = input("Enter issue: ")
            self.chosen_paper.issue = issue
            self.save_paper()

    def add_pages(self):
        """Add(overwrite) pages to :attr:`Paper.pages` attribute of chosen :class:`Paper`."""
        if self.chosen_paper:
            pages = input("Enter pages: ")
            self.chosen_paper.pages = pages
            self.save_paper()

    def add_doi(self):
        """Add(overwrite) doi to :attr:`Paper.doi` attribute of chosen :class:`Paper`.

        When given a correct doi address, `urllib` connects to the api of `crossref.org`
        web site and saves desired :class:`Paper` attributes automaticly.

        """

        if self.chosen_paper:
            doi = input("Enter doi: ")
            self.chosen_paper.doi = doi
            # automatic insert
            url = "https://api.crossref.org/v1/works/{0}".format(doi)
            response = urllib.urlopen(url)
            data = json.load(response)
            if data['status'] == "ok" and 'message' in data:
                authors = []
                if 'author' in data['message']:
                    for name in data['message']['author']:
                        authors.append("{0} {1}".format(name['given'], name['family']))
                if 'title' in data['message']: self.chosen_paper.title = data['message']['title'][0]
                if authors: self.chosen_paper.author = ", ".join(authors)
                if 'created' in data['message']: self.chosen_paper.year = str(data['message']['created']['date-parts'][0][0])
                if 'short-container-title' in data['message']: self.chosen_paper.journal = data['message']['short-container-title'][0]
                if 'volume' in data['message']: self.chosen_paper.volume = data['message']['volume']
                if 'issue' in data['message']: self.chosen_paper.issue = data['message']['issue']
                if 'page' in data['message']: self.chosen_paper.pages = data['message']['page']
            self.save_paper()

    def add_url(self):
        """Add(overwrite) url to :attr:`Paper.url` attribute of chosen :class:`Paper`.

        If given an arXiv URL, `urllib` connects to the api of `arXiv.org`
        web site and saves desired :class:`Paper` attributes automaticly.

        """

        if self.chosen_paper:
            url = input("Enter url: ")
            self.chosen_paper.url = url
            # automatic insert for arxiv links
            if "arxiv" in url.lower():
                arxiv_id = re.findall("\d+\.\d+", url)
                if arxiv_id:
                    arxiv_api_url = "http://export.arxiv.org/api/query?id_list={0}".format(arxiv_id[0])
                    data = urllib.urlopen(arxiv_api_url)
                    root = ET.parse(data).getroot()
                    entry = root.find('{http://www.w3.org/2005/Atom}entry')
                    authors = [author.find('{http://www.w3.org/2005/Atom}name').text
                                    for author in entry.findall('{http://www.w3.org/2005/Atom}author')]
                    self.chosen_paper.title = entry.find('{http://www.w3.org/2005/Atom}title').text
                    self.chosen_paper.author = ", ".join(authors)
                    self.chosen_paper.year = str(entry.find('{http://www.w3.org/2005/Atom}published').text)[:4]
                    self.chosen_paper.journal = 'arXiv{0}'.format(arxiv_id[0])
            self.save_paper()

    def add_comment(self):
        """Add(overwrite) comment to :attr:`Paper.comment` attribute of chosen :class:`Paper`."""
        if self.chosen_paper:
            comment = input("Enter your comment: ")
            self.chosen_paper.comment = comment
            self.save_paper()

    def add_collection(self, collection_id):
        """Add(overwrite) collection to :attr:`Paper.collection` attribute of chosen :class:`Paper`.

        This method does not check if given :arg:`collection_id` value truly exists for any 
        :attr:`Collection.id` attributes of :class:`Collection` instances, it should be 
        checked outside of this class (e.g. :class:`menu`).

        """

        if self.chosen_paper:
            self.chosen_paper.collection_id = collection_id
            self.save_paper()

    def save_paper(self):
        """Save a unique id number if the object is a newly instantiated :class:`Paper` object.

        Then append this :class:`Paper` to :attr:`PaperMark.papers` :obj:`list`, update
        `json` data file by calling :meth:`PaperMark.save_json()` and at last uptade the order of 
        :class:`Paper` instances in :attr:`PaperMark.papers` :obj:`list` by calling 
        :meth:`PaperMark.sort()`.

        """

        if self.chosen_paper:
            if self.chosen_paper.save_id_for_new():
                self.papers.append(self.chosen_paper)
            # Save to json file.
            self.save_json()
            self.sort()
    
    def sort(self):
        """Sort :attr:`papers` :obj:`list` by attr:`Paper.year` in descending order."""
        self.papers = sorted(self.papers, key=lambda paper: paper.year, reverse=True)

    def delete(self):
        if self.chosen_paper:
            if self.chosen_paper in self.papers:
                self.papers.remove(self.chosen_paper)
                self.save_json()
            self.chosen_paper = None

    def save_json(self):
        """Save a `json` file holding all :class:`Paper` instance attributes in `json` data format."""
        if len(self.papers) > 0:
                with open('./data/papers.json', 'w') as output_file:
                    json.dump([paper.__dict__ for paper in self.papers], output_file)
                output_file.close()


    def search_papers(self, filter):
        """Check if `filter` matches with some attributes of undeleted :class:`Paper` instances."""
        return [paper for paper in self.papers if
                paper.match(filter)]