import sys
from paper import PaperMark, CollectionHolder
from os.path import exists as PathExists
from os import makedirs as MakeDirs


class Menu(object):
    def __init__(self):
        global input
        global raw_input
        try: input = raw_input
        except NameError: pass
        if not PathExists('./pages'):
            MakeDirs('./pages')
        if not PathExists('./data'):
            MakeDirs('./data')
        self.papermark = PaperMark()
        self.collection_holder = CollectionHolder()
        self.choices = {
                "1" : self.search_papers,
                "2" : self.add_paper,
                "3" : self.choose_paper_by_id,
                "4" : self.show_collections,
                "5" : self.search_collections,
                "6" : self.add_new_collection,
                "7" : self.choose_collection_by_id,
                "8" : self.create_papermark_pages,
                "9" : self.quit
                }
        self.paper_choices = {
                "1" : self.papermark.add_title,
                "2" : self.papermark.add_author,
                "3" : self.papermark.add_journal,
                "4" : self.papermark.add_volume,
                "5" : self.papermark.add_year,
                "6" : self.papermark.add_issue,
                "7" : self.papermark.add_pages,
                "8" : self.papermark.add_doi,
                "9" : self.papermark.add_url,
                "10" : self.papermark.add_comment,
                "11" : self.add_collection_to_paper,
                "12" : self.delete_paper,
                "13" : self.run
                }
        self.collection_choices = {
                "1" : self.collection_holder.add_name,
                "2" : self.collection_holder.add_comment,
                "3" : self.collection_holder.add_order_number,
                "4" : self.delete_collection,
                "5" : self.run
        }
        print("""











 _ _ _  ___ | | ___  ___ ._ _ _  ___   _| |_ ___ 
| | | |/ ._>| |/ | '/ . \| ' ' |/ ._>   | | / . \\
|__/_/ \___.|_|\_|_.\___/|_|_|_|\___.   |_| \___/
                                                 
 ___  ___  ___  ___  ___  __ __  ___  ___  _ __
| . \| . || . \| __>| . \|  \  \| . || . \| / /
|  _/|   ||  _/| _> |   /|     ||   ||   /|  \ 
|_|  |_|_||_|  |___>|_\_\|_|_|_||_|_||_\_\|_\_\\

""")

    def display_menu(self):
        print("""
Papermark Menu ---------------------------

1. Search Papers
2. Add New Paper
3. Choose Paper by ID Number
--
4. Show Collections
5. Search Collections
6. Add New Collection
7. Choose Collection by ID Number
--
8. Create(Update) Papermark Page
--
9. Quit
------------------------------------------
""")

    def run(self):
        while True:
            self.display_menu()
            choice = input('Enter an option: ')
            action = self.choices.get(choice)
            if action:
                action()
            else:
                print("""
------------------------------------------

{0} is not a valid choice.

------------------------------------------
""".format(choice))

    def show_papers(self, papers=None):
        print("""









Papers:
""")
        if not papers:
            print("""
------------------------------------------

 0 papers found.

------------------------------------------

""")
        else:
            for paper in papers:
    
                not_assigned = '...'
                paper_id = paper.id if paper.id else not_assigned
                paper_creation_date = paper.creation_date if paper.creation_date else not_assigned
                paper_title = paper.title if paper.title else not_assigned
                paper_author = paper.author if paper.author else not_assigned
                paper_journal = paper.journal if paper.journal else not_assigned
                paper_volume = paper.volume if paper.volume else not_assigned
                paper_year = paper.year if paper.year else not_assigned
                paper_pages = paper.pages if paper.pages else not_assigned
                paper_comment = paper.comment if paper.comment else not_assigned
                collection_id = not_assigned
                collection_name = not_assigned
                if paper.collection_id:
                    self.choose_collection_by_id(paper.collection_id)
                    collection = self.collection_holder.chosen_collection
                    if collection:
                        collection_id =collection.id
                        collection_name = collection.name
                print("""
id: {0}, date: {1}
------------------------------------------
 title: {2}\n author: {3}\n {4} {5} ({6}) {7}
------------------------------------------
collection: {8}(id: {9})
comment: {10}

""".format(paper_id, paper_creation_date, paper_title, paper_author, 
                    paper_journal, paper_volume, paper_year, paper_pages, 
                    collection_name, collection_id, paper_comment))

    def show_collections(self, collections=None):
        print("""









Collections:
""")
        if collections == None:
            collections = self.collection_holder.collections
        if len(collections) > 0:
            for collection in collections:
                if collection.deleted == 0:
                    not_assigned = '...'
                    collection_id = collection.id if collection.id else not_assigned
                    collection_name = collection.name if collection.name else not_assigned
                    collection_comment = collection.comment if collection.comment else not_assigned
                    collection_order_num = collection.order_num if collection.order_num else not_assigned
                    print("""
------------------------------------------
id: {0}, order number: {1}
name: {2}
comment: {3}
------------------------------------------

""".format(collection_id, collection_order_num, collection_name, collection_comment))
        else:
            print("""
------------------------------------------

0 collections found.

------------------------------------------
""")

    def search_papers(self):
        filter = input("Search for: ")
        papers = self.papermark.search_papers(filter)
        self.show_papers(papers)
        self.run()

    def search_collections(self):
        filter = input("Search for: ")
        collections = self.collection_holder.search_collections(filter)
        self.show_collections(collections)
        self.run()

    def add_paper(self):
        self.papermark.new_paper()
        print("""
------------------------------------------

New paper created.

------------------------------------------
""")
        self.run_paper_menu()

    def add_collection_to_paper(self):
        id_number = int(input("Enter collection id number(\"0\" to free from collections): "))
        if id_number == 0:
            self.papermark.chosen_paper.collection_id = None
        else:
            chosen_collection = None
            for collection in self.collection_holder.collections:
                if collection.id == id_number:
                    chosen_collection = collection
            if chosen_collection:
                self.papermark.add_collection(chosen_collection.id)
                print('Paper is in the collection: {0}'.format(chosen_collection.name))
            else:
                print('No collection found.')
        self.run_paper_menu()

    def add_new_collection(self):
        self.collection_holder.new_collection()
        print("""
------------------------------------------

New collection created.

------------------------------------------
""")
        self.run_collection_menu()

    def run_paper_menu(self):
        while True:
            self.show_papers([self.papermark.chosen_paper])
            self.display_paper_menu()
            choice = input("Enter an option: ")
            action = self.paper_choices.get(choice)
            if action:
                action()
            else:
                print("""
------------------------------------------

{0} is not a valid choice.

------------------------------------------
""".format(choice))

    def run_collection_menu(self):
        if self.collection_holder.chosen_collection:
            while True:
                self.show_collections([self.collection_holder.chosen_collection])
                self.display_collection_menu()
                choice = input("Enter an option: ")
                action = self.collection_choices.get(choice)
                if action:
                    action()
                else:
                    print("""
------------------------------------------

{0} is not a valid choice.

------------------------------------------
""".format(choice))
        else:
            self.show_collections([])
            self.run()

    def display_paper_menu(self):
        print("""
Paper Menu -------------------------------

Add(Edit):
1. Title | 2. Author | 3. Journal | 4. Volume | 5. Year
6. Issue | 7. Pages | 8. DOI | 9. URL |10. Add Comment
11. Add to Collection | 12. Delete Paper
--
13. Back to Main Menu
------------------------------------------
""")

    def display_collection_menu(self):
        print("""
Collection Menu --------------------------

Add(Edit):
1. Name | 2. Comment | 3. Order Number | 4. Delete Collection
--
5. Back to Main Menu
------------------------------------------
""")

    def choose_paper_by_id(self):
        id_number = int(input("Enter id number: "))
        self.papermark.choose_by_id(id_number)
        if self.papermark.chosen_paper:
            self.run_paper_menu()
        else:
            print("""
------------------------------------------

No papers found.

------------------------------------------
""")

    def choose_collection_by_id(self, collection_id=None):
        if collection_id:
            id_number = collection_id
        else:
            id_number = int(input("Enter id number: "))
        self.collection_holder.choose_by_id(id_number)
        """
        If collection_id is not provided via the argument, display the collection and the menu.
        Otherwise just the program demands the collection with that id to use it, do not display anything.
        """
        if not collection_id:
            self.run_collection_menu()

    def delete_paper(self):
        choice = input("Are you sure?(\"yes\" to delete): ")
        if choice.lower() == "yes":
            self.papermark.delete()
            self.run()

    def delete_collection(self):
        choice = input("Are you sure?(\"yes\" to delete): ")
        if choice.lower() == "yes":
            self.collection_holder.delete()
            self.run()

    def create_papermark_pages(self):
        """
        Creates a publishable markdown page for collections
        and papers.
        """
        head_str = """# My Reading List of Papers

"""
        body_str = ''
        collections = self.collection_holder.collections
        papers = self.papermark.papers
        if len(collections) > 0:
            for collection in collections:
                if collection.deleted == 0:
                    paper_list = [paper for paper in papers if paper.collection_id == collection.id]
                    if paper_list:
                        body_str = body_str + '### ' + collection.name + """:

"""
                        if collection.comment:
                            body_str = body_str + '*' + collection.comment + """*
"""
                        for index, paper in enumerate(paper_list):
                            author = '. *' + paper.author + '*' if paper.author else ''
                            title = paper.title if paper.title else ''
                            journal = '. ' + paper.journal if paper.journal else ''
                            volume = ' ' + paper.volume if paper.volume else ''
                            year = ' (' + paper.year + ')' if paper.year else ''
                            pages = ' ' + paper.pages if paper.pages else ''
                            if paper.url:
                                url = """
    * **url**: """ + '[' + paper.url + ']' + '(' + paper.url + ')'
                            else:
                                url = ''
                            if paper.doi:
                                doi = """
    * **doi**: """ + '[' + paper.doi + ']' + '(' + paper.doi + ')'
                            else:
                                doi = ''
                            if paper.comment:
                                comment = """
    * **comment**: """ + paper.comment
                            else:
                                comment = ''
                            body_str = body_str + str(index + 1) + '. ' + title + author + journal + \
                            volume + year + pages + doi + url + comment + """

"""
        body_str = body_str + """
-
*Created with [papermark](https://github.com/wphw/papermark/).*"""
        with open('./pages/reading-list.md', 'w') as file:
            file.write(head_str + body_str)
        file.close()
        print("""
------------------------------------------

Papermark page created(updated).

------------------------------------------
""")





    def quit(self):
        print("""
------------------------------------------

Papermark closed.

------------------------------------------
""")
        sys.exit(0)




Menu().run()