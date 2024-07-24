import json
from typing import List

# DO NOT MODIFY!
class Node():
    def __init__(self,
                 key : int,
                 word : str,
                 leftchild,
                 rightchild):
        self.key = key
        self.word = word
        self.leftchild = leftchild
        self.rightchild = rightchild

# DO NOT MODIFY!
def dump(root: Node) -> str:
    def _to_dict(node) -> dict:
        return {
            "key": node.key,
            "word": node.word,
            "l": (_to_dict(node.leftchild) if node.leftchild is not None else
            None),
            "r": (_to_dict(node.rightchild) if node.rightchild is not None else
            None)
        }
    if root == None:
        dict_repr = {}
    else:
        dict_repr = _to_dict(root)
    return json.dumps(dict_repr,indent = 2)


def get_height(node):
    if node is None:
        return 0
    left_height = get_height(node.leftchild)
    right_height = get_height(node.rightchild)
    return max(left_height, right_height) + 1


def update_height(node):
    if node is not None:
        node_height = 1 + max(get_height(node.leftchild), get_height(node.rightchild)) 
        return node_height 
    else:
        return 0


def left_rotate(x):
    y = x.rightchild
    T2 = y.leftchild

    y.leftchild = x
    x.rightchild = T2

    if x is None:
        return
    update_height(x)

    if y is None:
        return
    update_height(y)

    return y

def right_rotate(y):
    x = y.leftchild
    T2 = x.rightchild

    x.rightchild = y
    y.leftchild = T2

    if y is None:
        return
    update_height(y)
    
    if x is None:
        return
    update_height(x)

    return x

# insert
# For the tree rooted at root, insert the given key,word pair and then balance as
#per AVL trees.
# The key is guaranteed to not be in the tree.
# Return the root.
def insert(root: Node, key: int, word: str) -> Node:
    if root is None:
        return Node(key, word, None, None)
    
    if key < root.key:
        root.leftchild = insert(root.leftchild, key, word)
    else:
        root.rightchild = insert(root.rightchild, key, word)

    update_height(root)
    if root is not None:
        balance = get_height(root.leftchild) - get_height(root.rightchild)
    else: 
        balance = 0


    # Left Heavy
    if balance > 1:
        if key < root.leftchild.key:
            return right_rotate(root)
        else:
            root.leftchild = left_rotate(root.leftchild)
            return right_rotate(root)

    # Right Heavy
    if balance < -1:
        if key > root.rightchild.key:
            return left_rotate(root)
        else:
            root.rightchild = right_rotate(root.rightchild)
            return left_rotate(root)

    return root

def get_balance(node):
    if node is None:
        return 0
    left_height = get_height(node.leftchild)
    right_height = get_height(node.rightchild)
    return left_height - right_height


def preorderInsert(root: Node, items: List) -> list:
    if root:
        items.append((root.key,root.word))
        preorderInsert(root.leftchild, items)
        preorderInsert(root.rightchild,items)
    return items 

# bulkInsert
# The parameter items should be a list of pairs of the form [key,word] where key is
#an integer and word is a string.
# For the tree rooted at root, first insert all of the [key,word] pairs as if the
#tree were a standard BST, with no balancing.
# Then do a preorder traversal of the [key,word] pairs and use this traversal to
#build a new tree using AVL insertion.
# Return the root
def bulkInsert(root: Node, items: List) -> Node:
    preorderlst = []
    def insertBulk(root: Node, key: int, word: str):
        if root is not None:
            key = int(key)
            root.key = int(root.key)

        if root is None:
            return Node(key, word, None, None)
        elif key < root.key:
            root.leftchild = insertBulk(root.leftchild, key, word)
        else:
            root.rightchild = insertBulk(root.rightchild, key, word)

        return root
    
    for key, word in items:
        root = insertBulk(root, key, word)
    
    
    preorderlst = preorderInsert(root, preorderlst)
    
    new_root = None 
    for item in preorderlst:
        new_root = insert(new_root,item[0],item[1])

    return new_root

def preorderDelete(root, new_tree_root, lst):
    if root:
        if root.key not in lst:
            new_tree_root = insert(new_tree_root, root.key, root.word)
            
        new_tree_root = preorderDelete(root.leftchild, new_tree_root, lst)
        new_tree_root = preorderDelete(root.rightchild, new_tree_root, lst)
        
    return new_tree_root

# bulkDelete
# The parameter keys should be a list of keys.
# For the tree rooted at root, first tag all the corresponding nodes (however you
#like),
# Then do a preorder traversal of the [key,word] pairs, ignoring the tagged nodes,
# and use this traversal to build a new tree using AVL insertion.
# Return the root.
def bulkDelete(root: Node, keys: List[int]) -> Node:
    tagged_nodes = set(keys)
    
    new_root = None
    
    new_root = preorderDelete(root, new_root, tagged_nodes)
    
    return new_root


# search
# For the tree rooted at root, calculate the list of keys on the path from the root
#to the search_key,
# including the search key, and the word associated with the search_key.
# Return the json stringified list [key1,key2,...,keylast,word] with indent=2.
# If the search_key is not in the tree return a word of None.
def search(root: Node, search_key: int) -> str:
    def find_path(node, key):
        if node is None:
            return None
        path = []

        while node is not None:
            path.append(node.key)
            if key == node.key:
                path.append(node.word)
                return path
            elif key < node.key:
                node = node.leftchild
            else:
                node = node.rightchild

        return None

    path = find_path(root, search_key)

    if path is not None:
        return json.dumps(path, indent=2)
    else:
        return json.dumps([None], indent=2)


# replace
# For the tree rooted at root, replace the word corresponding to the key search_key
#by replacement_word.
# The search_key is guaranteed to be in the tree.
# Return the root
def replace(root: Node, search_key: int, replacement_word: str) -> Node:
    curr_root = root 
    
    while curr_root is not None: 
        if curr_root.key == search_key:
            curr_root.word = replacement_word
            return root 
        elif curr_root.key < search_key:
            curr_root = curr_root.rightchild
        else:
            curr_root = curr_root.leftchild
    return root



