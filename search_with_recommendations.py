import sys
import json
import boolean
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import recommender
from nltk.stem import PorterStemmer
import string
letters = list(string.ascii_lowercase)
letters.append(list(string.ascii_uppercase))

stemmer=PorterStemmer()



class Conversion:
    def __init__(self, capacity):
        self.top = -1 
        self.capacity = capacity
        self.array = []
        self.output = []
        self.precedence = {'|':1, '&':2, '~':3}

    def isEmpty(self):
        return True if self.top == -1 else False
      
    def peek(self):
        return self.array[-1]

    def pop(self):
        if not self.isEmpty():
            self.top -= 1
            return self.array.pop()
        else:
            return "$"

    def push(self, op):
        self.top += 1
        self.array.append(op) 
  
    def isOperand(self, ch):
        return ch.isalpha()

    def notGreater(self, i):
        try:
            a = self.precedence[i]
            b = self.precedence[self.peek()]
            return True if a  <= b else False
        except KeyError: 
            return False

    def infixToPostfix(self, exp):
        for i in exp:
            if self.isOperand(i):
                self.output.append(i)

            elif i  == '(':
                self.push(i)

            elif i == ')':
                while( (not self.isEmpty()) and 
                                self.peek() != '('):
                    a = self.pop()
                    self.output.append(a)
                if (not self.isEmpty() and self.peek() != '('):
                    return -1
                else:
                    self.pop()

            else:
                while(not self.isEmpty() and self.notGreater(i)):
                    self.output.append(self.pop())
                self.push(i)
  
        while not self.isEmpty():
            self.output.append(self.pop())
  
        return "".join(self.output)


class Parse():
    def __init__(self, query):
        self.query = query

    def transform(self):
        split_query = self.query.split(" ")

        for i in range(0, len(split_query)):
            if(split_query[i] != "and" and split_query[i] != "or" and split_query[i] != "not"):
                split_query[i] = split_query[i] + 'sep'
        
        self.query = " ".join(split_query)

    def parser(self):
        
        self.transform()

        algebra = boolean.BooleanAlgebra()
        try:
            res = algebra.parse(self.query)
        except SyntaxError:
            raise SyntaxError("Invalid syntax in query")
        self.query = str(res)
        self.convert_to_postfix()
        return self.query
    
    def convert_to_postfix(self):
        q = Conversion(len(self.query))
        self.query = q.infixToPostfix(self.query)


class Execute:
    def __init__(self, capacity, vocab):
        self.top = -1
        self.capacity = capacity
        self.array = []
        self.vocab = vocab
      
    def isEmpty(self):
        return True if self.top == -1 else False
      
    def peek(self):
        return self.array[-1]
      
    def pop(self):
        if not self.isEmpty():
            self.top -= 1
            return self.array.pop()
        else:
            return "$"
      
    def push(self, op):
        self.top += 1
        self.array.append(op) 

    def exec(self, exp):
        op = Operators(self.vocab)
        exp = exp.split("sep")
        try:
            if(exp[2][0] == '&' and exp[2][1] in letters or exp[2][0] == '|' and exp[2][1] in letters or exp[2][0] == '~' and exp[2][1] in letters):
                c = exp[2][0]
                exp[2] = exp[2][1:]
                exp[3] = exp[3] + c
        except:
            pass

        for i in exp:
            if '&' not in i and '|' not in i and '~' not in i:
                try:
                    self.push(self.vocab[stemmer.stem(i)])
                except KeyError:
                    return ["Does not exist in the database"]
                
            else:

                for char in i:
                    if(char == '&'):
                        val1 = self.pop()
                        val2 = self.pop()
                        res = op.intersection(val1, val2)

                    elif(char == '~'):
                        val1 = self.pop()
                        res = op.diff(val1)
                    else:
                        val1 = self.pop()
                        val2 = self.pop()
                        res = op.union(val1, val2)


                    self.push(res)
  
        temp = self.pop()
        self.array = []
        return temp
                  

class Operators:
    def __init__(self, global_vocab):
        self.vocab = global_vocab
    
    def intersection(self, operand1, operand2):
        return list(set(operand1) & set(operand2)) 

    def union(self, operand1, operand2):
        return list(set(operand1).union(set(operand2)))
    
    def diff(self, operand1):
        return (list(list(set(self.vocab)-set(operand1)) + list(set(operand1)-set(self.vocab))))


class BuildIndex:
    def __init__(self, index):
        self.index = index
    
    def check_key(self, key, global_vocab):
        if key in global_vocab:
            return True
        return False

    def build(self):
        global_vocab = {}
        for term in self.index:
            if not self.check_key(term, global_vocab):
                global_vocab[term] = []
            for movies in self.index[term]:
                if movies not in global_vocab[term]:
                    global_vocab[term].append(movies)
        
        return global_vocab


if __name__ == "__main__":
    with open('index.json', 'r') as fp:
        index = json.load(fp)

    vocab = BuildIndex(index).build()
    
    '''Initialisation of matrices for peforming reccomendation'''
    data=pd.read_csv("tmdb_5000_movies.csv")
    '''
    Recommendation by performing cosine similarity
    on tf-idf vectors generated from the overviews
    of movies. Before performing tf-idf vectorization, define vectorizer to remove english
    stop words
    '''
    tfidf_vectorizer=TfidfVectorizer(stop_words='english')
    '''
    Fill up NA overviews
    '''
    data['overview']=data['overview'].fillna('')
    '''
    Construction of the tf-idf matrix
    It is a sparse matrix:
    (document_id, token_id) , tf_idf score
    '''
    tfidf_matrix=tfidf_vectorizer.fit_transform(data['overview'])
    '''
    Calculating cosine similarity
    '''
    cosine_sim=cosine_similarity(tfidf_matrix,tfidf_matrix)
    '''
    Mapping movie titles to index
    '''
    
    rec_index=pd.Series(data.index, index=data['title']).drop_duplicates()
    
    #print(get_reccomendation(data,movie_name,index,cosine_sim))
    query = input("QUERY: ")


    while query != "exit" and query != "quit":
        parsed_query = Parse(query).parser()
        
        results = Execute(len(parsed_query), vocab).exec(parsed_query)
        print("RESULT:")
        if(len(results) == 0):
            print("No matching results found")
        else:
            for result in results:
                print(result)
                
            print("\nOther Suitable Recommendations:")    
            for result in results:
                if result != "Does not exist in the database":
                    try:
                        x=recommender.get_reccomendation(data,result,rec_index,cosine_sim)
                        print("\nRecommendations for",result,"->")
                        for i, m in enumerate(x):
                            print((i+1), "-->",m)
                    except:
                        print("None")
                else:
                    print("None")
        print("\n")

        query = input("QUERY: ")
        if(query == "exit" or query == "quit"):
            sys.exit(0)
            
    sys.exit(0)
    
