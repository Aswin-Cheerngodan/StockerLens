from langchain_community.document_loaders import WebBaseLoader
loader_multiple_pages = WebBaseLoader(
    ['https://www.geeksforgeeks.org/data-structures/', 'https://www.techtarget.com/searchdatamanagement/definition/data-structure', 'https://www.reddit.com/r/learnprogramming/comments/103j1bn/what_is_a_data_structure/']
)


if __name__=="__main__":
    docs = loader_multiple_pages.load()
    print(docs[0])