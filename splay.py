from __future__ import annotations
import json
from typing import List

verbose = False

# DO NOT MODIFY!
class Node():
    def  __init__(self,
                  key       : int,
                  leftchild  = None,
                  rightchild = None,
                  parent     = None,):
        self.key        = key
        self.leftchild  = leftchild
        self.rightchild = rightchild
        self.parent     = parent

# DO NOT MODIFY!
class SplayTree():
    def  __init__(self,
                  root : Node = None):
        self.root = root
        

    # For the tree rooted at root:
    # Return the json.dumps of the object with indent=2.
    # DO NOT MODIFY!
    def dump(self) -> str:
        def _to_dict(node) -> dict:
            pk = None
            if node.parent is not None:
                pk = node.parent.key
            return {
                "key": node.key,
                "left": (_to_dict(node.leftchild) if node.leftchild is not None else None),
                "right": (_to_dict(node.rightchild) if node.rightchild is not None else None),
                "parentkey": pk
            }
        if self.root == None:
            dict_repr = {}
        else:
            dict_repr = _to_dict(self.root)
        return json.dumps(dict_repr,indent = 2)





    #1. first step is to call splay(x) and if x is not in the tree, (guaranteed 
    # to not be in the tree) get the IOP or IOS of x. (we can use IOP) 
    #2. Then call splay on this IOP and brings it to the root, and 
    # rebalances tree correctly 
    #3. then put the node we wanted to insert (x) at the root, and 
    # hang the 57 and its left subtree to the left of the new node, and the 
    # right subtree of 57 to the right of the new node.

    #Function to find IOS/IOP:
    def find_next(self, root, key):
        predecessor = None
        successor = None
        curr = None

        while root:
            if root.key == key:
                # Find the rightmost node in the left subtree 
                if root.leftchild:
                    predecessor = root.leftchild
                    while predecessor.rightchild:
                        predecessor = predecessor.rightchild
                    
                # Find the leftmost node in the right subtree 
                if root.rightchild:
                    successor = root.rightchild
                    while successor.leftchild:
                        successor = successor.leftchild
                
                return predecessor if predecessor else successor
                # Return the predecessor if it exists, otherwise return the successor
                

            elif key < root.key:
                successor = root 
                predecessor = root
                root = root.leftchild
            else:
                predecessor = root 
                successor = root
                root = root.rightchild

        return predecessor if predecessor else successor
  


    # Insert Method 1
    def insert(self, key: int):

        new_node = Node(key=key)    
        if self.root is None:
            self.root = new_node
            return 
        
        # Guaranteed to not be in the tree so find the IOS of x. IOS of x = y
        y = self.find_next(self.root, key)
        # bring y to the root
        self.splay(y)
        
        if key < self.root.key:
            new_node.leftchild = self.root.leftchild
            if new_node.leftchild:
                new_node.leftchild.parent = new_node
            new_node.rightchild = self.root
            self.root.leftchild = None
            self.root.parent = new_node
        else:
            new_node.rightchild = self.root.rightchild
            if new_node.rightchild:
                new_node.rightchild.parent = new_node
            new_node.leftchild = self.root
            self.root.rightchild = None
            self.root.parent = new_node

        self.root = new_node

    def splay(self, x: Node) -> Node:
        while x.parent is not None:
            parent_x = x.parent
            grandparent_x = parent_x.parent 

            # Zig case
            if grandparent_x is None: 
                #self.root.leftchild and self.root.leftchild.key == x:
                if x == parent_x.leftchild:
                    self.right_rotate(parent_x)
                else:
                    self.left_rotate(parent_x)
                #elif self.root.rightchild and self.root.rightchild.key == x:
                    #self.left_rotate(self.parent)
            else:
                # Zig-Zig and Zig-Zag cases
                if x == parent_x.leftchild and parent_x == grandparent_x.leftchild:
                    self.right_rotate(grandparent_x)
                    self.right_rotate(parent_x)
                #if x < self.root.key:
                    # Node is in left subtree of root
                elif x == parent_x.rightchild and parent_x == grandparent_x.rightchild:
                    self.left_rotate(grandparent_x)
                    self.left_rotate(parent_x)
                else:
                    if x == parent_x.leftchild:
                       self.right_rotate(parent_x)
                       self.left_rotate(grandparent_x)
                    else:
                        self.left_rotate(parent_x)
                        self.right_rotate(grandparent_x)
                    
        if x is not None:
            self.root = x         
            

    def insert_BST(self, root: Node, key: int) -> Node:
        if root is None:
            return Node(key)
        elif key < root.key:
            root.leftchild = self.insert_BST(root.leftchild, key)
        else:
            root.rightchild = self.insert_BST(root.rightchild, key)

        return root


    def left_rotate(self, node: Node):
        right_child = node.rightchild
        if right_child:
            node.rightchild = right_child.leftchild
            if right_child.leftchild:
                right_child.leftchild.parent = node
            right_child.parent = node.parent
            if not node.parent:
                self.root = right_child
            elif node == node.parent.leftchild:
                node.parent.leftchild = right_child
            else:
                node.parent.rightchild = right_child
            right_child.leftchild = node
            node.parent = right_child

        return right_child


    
    def right_rotate(self, node: Node):
        left_child = node.leftchild 
        if left_child:
            node.leftchild = left_child.rightchild 
            if left_child.rightchild:
                left_child.rightchild.parent = node 
            left_child.parent = node.parent

            if not node.parent:
                self.root = left_child 
            elif node == node.parent.rightchild:
                node.parent.rightchild = left_child 
            else:
                node.parent.leftchild = left_child 
            
            left_child.rightchild = node 
            node.parent = left_child 
        return left_child



    def get_height(self, node):
        if node is None:
            return 0
        left_height = self.get_height(node.leftchild)
        right_height = self.get_height(node.rightchild)
        return max(left_height, right_height) + 1


    def update_height(self,node):
        if node is not None:
            node_height = 1 + max(self.get_height(node.leftchild), self.get_height(node.rightchild)) 
            return node_height 
        else:
            return 0
    

     # Search
    def search(self,key:int):
        x = self.root
        last = self.root
        while x:
            last = x
            if key == x.key:
                self.splay(x)
                return x
            elif key < x.key:
                x = x.leftchild
            else:
                x = x.rightchild
        self.splay(last)
        return None
        


    def min(self, x):
        while x.leftchild != None:
            x = x.leftchild
        return x


    def find(self, key):
        if not self.root:
            return None
        node = self.find_helper(self.root, key)
        if node:
            self.splay(node)
        return node

    def find_helper(self, node, key):
        if not node or node.key == key:
            return node
        if key < node.key:
            if not node.leftchild:
                return node
            return self.find_helper(node.leftchild, key)
        else:
            if not node.rightchild:
                return node
            return self.find_helper(node.rightchild, key)

    # Delete Method 1
    def delete(self,key:int):
        target = self.find(key)
        self.splay(target)

        #check if target has a leftchild and not a rightchild
            #if it does, leftchild goes to parent 
        if self.root.leftchild is not None and self.root.rightchild is None:
            self.root = self.root.leftchild
            self.root.parent = None 
        
        #check if target has a rightchild and not a leftchild 
            #if it does, rightchild goes to parent 
        elif self.root.rightchild is not None and self.root.leftchild is None:
            self.root = self.root.rightchild
            self.root.parent = None 

        #if there is both a left and right child
            #call splay on right
            #promote right subtree to root 
        else:
            min = self.min(target.rightchild)
            if min:
                self.splay(min)
                self.root = min 
                #print(self.root.leftchild.key)
                #print(target.leftchild.key)
                self.root.leftchild = target.leftchild
                #print(self.root.leftchild.key)
                self.root.parent = self.root 
                #print(self.root.parent.key)
                self.root.leftchild.parent = self.root
                self.root.parent = None
            
        
    def print_tree(self, node, level=0):
        if node:
            print("Level", level, ":", node.key)
            if node.leftchild:
                self.print_tree(node.leftchild, level + 1)
            if node.rightchild:
                self.print_tree(node.rightchild, level + 1)

    

   

"""
splaytree = SplayTree()
splaytree.insert(30)
splaytree.insert(15)
splaytree.insert(26)
splaytree.insert(46)
splaytree.insert(14)
splaytree.print_tree(splaytree.root)
print('\n')
"""
