from __future__ import annotations
import json
import math
from typing import List
import heapq
from queue import PriorityQueue



# Datum class.
# DO NOT MODIFY.
class Datum():
    def __init__(self,
                 coords : tuple[int],
                 code   : str):
        self.coords = coords
        self.code   = code
    def to_json(self) -> str:
        dict_repr = {'code':self.code,'coords':self.coords}
        return(dict_repr)

# Internal node class.
# DO NOT MODIFY.
class NodeInternal():
    def  __init__(self,
                  splitindex : int,
                  splitvalue : float,
                  leftchild,
                  rightchild):
        self.splitindex = splitindex
        self.splitvalue = splitvalue
        self.leftchild  = leftchild
        self.rightchild = rightchild

# Leaf node class.
# DO NOT MODIFY.
class NodeLeaf():
    def  __init__(self,
                  data : List[Datum]):
        self.data = data

# KD tree class.
class KDtree():
    def  __init__(self,
                  k    : int,
                  m    : int,
                  root = None):
        self.k    = k
        self.m    = m
        self.root = root

    # For the tree rooted at root, dump the tree to stringified JSON object and return.
    # DO NOT MODIFY.
    def dump(self) -> str:
        def _to_dict(node) -> dict:
            if isinstance(node,NodeLeaf):
                return {
                    "p": str([{'coords': datum.coords,'code': datum.code} for datum in node.data])
                }
            else:
                return {
                    "splitindex": node.splitindex,
                    "splitvalue": node.splitvalue,
                    "l": (_to_dict(node.leftchild)  if node.leftchild  is not None else None),
                    "r": (_to_dict(node.rightchild) if node.rightchild is not None else None)
                }
        if self.root is None:
            dict_repr = {}
        else:
            dict_repr = _to_dict(self.root)
        return json.dumps(dict_repr,indent=2)

    # Insert the Datum with the given code and coords into the tree.
    # The Datum with the given coords is guaranteed to not be in the tree.

    def find_split(self, node):
        split = -1
        max_range = -1
        for split_dim in range(self.k):
            split_coords = [datum.coords[split_dim] for datum in node.data]
            min_coord, max_coord = min(split_coords), max(split_coords)
            spread = max_coord - min_coord
            if spread > max_range:
                max_range = spread
                split = split_dim

        #sort the points in the leaf according to that coordinate 
        #split them into the first floor(n/2) and then the rest 
        #splitting node is set to be the exact median 
        node.data.sort(key=lambda datum: datum.coords[split])

        median_index = len(node.data) // 2
        if len(node.data) % 2 == 0:
            split_value = float((node.data[median_index - 1].coords[split] + node.data[median_index].coords[split]) / 2)
        else:
            split_value = float(node.data[median_index].coords[split])

        return (split, split_value)
    

    def insert_helper(self, node, datum, depth):
        if isinstance(node, NodeLeaf):
            node.data.append(datum)
            if len(node.data) <= self.m:
                return node
            else:
                dim, split_value = self.find_split(node)
                left, right = [], []

                for datum in node.data:
                    if datum.coords[dim] < split_value:
                        left.append(datum)
                    else:
                        right.append(datum)

                left_leaf = NodeLeaf(left) if left else None
                right_leaf = NodeLeaf(right) if right else None

                return NodeInternal(dim, split_value, left_leaf, right_leaf)
        else:
            if datum.coords[node.splitindex] >= node.splitvalue:
                node.rightchild = self.insert_helper(node.rightchild, datum, depth + 1)
            else:
                node.leftchild = self.insert_helper(node.leftchild, datum, depth + 1)
            return node

    def insert(self,point:tuple[int],code:str):
        #outline:
        #follow the splitting nodes (less then go left otherwise go right)
        #if reach leaf node, insert the point 
        #ask if it is overfull 
            #if not overfull, nothing to do
            #if it is overfull:
                #create a parent splitting node
                #pick the coordinate such that the point spread in that coordinate’s direction is largest

                #sort the points in the leaf according to that coordinate 
                #split them into the first floor(n/2) and then the rest 
                #splitting node is set to be the exact median 
        
        if self.root is None:
            self.root = NodeLeaf([Datum(point, code)])
        else:
            self.root = self.insert_helper(self.root, Datum(point, code), 0)

    
    # Delete the Datum with the given point from the tree.
    # The Datum with the given point is guaranteed to be in the tree.
    def delete(self,point:tuple[int]):
        #outline
        #delete the point
        #if it becomes empty when deleted: 
            #remove the splitting node and connect the sibling of the empty leaf directly to the parent of the splitting node.
        self.root, _ = self.delete_empty(self.root, point, depth=0)

        if self.root is None:
            self.root = NodeLeaf([])

    
    def delete_empty(self, node, point, depth):
        if isinstance(node, NodeLeaf):
            node.data = [datum for datum in node.data if datum.coords != point]
            if len(node.data) == 0:
                return None, True  # Node is empty, should be removed
            return node, False  # Node is not empty, no need to recalculate split

        if isinstance(node, NodeInternal):
            if point[node.splitindex] < node.splitvalue:
                node.leftchild, child_altered = self.delete_empty(node.leftchild, point, depth + 1)
            else:
                node.rightchild, child_altered = self.delete_empty(node.rightchild, point, depth + 1)

            if child_altered:
                if node.leftchild is None or node.rightchild is None:
                    return (node.leftchild or node.rightchild), True
                

                if (isinstance(node.leftchild, NodeLeaf) and len(node.leftchild.data) < self.m / 2) and (isinstance(node.rightchild, NodeLeaf) and len(node.rightchild.data) < self.m / 2):
                    merged_data = node.leftchild.data + node.rightchild.data
                    return NodeLeaf(merged_data), True
                    
                    #return self.merge(node.leftchild, node.rightchild), True

            return node, False

        return node, False

    def empty(self, node):
        if isinstance(node, NodeInternal):
            if node.leftchild is None or node.rightchild is None:
                surviving_child = node.leftchild if node.leftchild is not None else node.rightchild
                if isinstance(surviving_child, NodeLeaf):
                    return surviving_child
            else:
                if (isinstance(node.leftchild, NodeLeaf) and len(node.leftchild.data) < self.m / 2) and (isinstance(node.rightchild, NodeLeaf) and len(node.rightchild.data) < self.m / 2):
                    merged_data = node.leftchild.data + node.rightchild.data
                    return NodeLeaf(merged_data)

        return node

    

    
    # Find the k nearest neighbors to the point.
    def knn(self,k:int,point:tuple[int]) -> str:
        # Use the strategy discussed in class and in the notes.
        # The list should be a list of elements of type Datum.
        # While recursing, count the number of leaf nodes visited while you
        #construct the list.
        # The following lines should be replaced by code that does the job. 
        
        def calc_bounding_box(subtree):
            if isinstance(subtree, NodeInternal):
                left_box = calc_bounding_box(subtree.leftchild)
                right_box = calc_bounding_box(subtree.rightchild)
                combined_box = tuple((min(left[0], right[0]), max(left[1], right[1])) for left, right in zip(left_box, right_box))
                return combined_box
            elif isinstance(subtree, NodeLeaf):
                dimensions = len(subtree.data[0].coords)
                bounds = [(float('inf'), -float('inf')) for _ in range(dimensions)]
                for datum in subtree.data:
                    for idx, coord in enumerate(datum.coords):
                        bounds[idx] = (min(bounds[idx][0], coord), max(bounds[idx][1], coord))
                return tuple(bounds)

        def search_knn(node, checked_leaves, nearest_list, num_neighbors, target_point):
            if isinstance(node, NodeInternal):
                if nearest_list:
                    max_dist = math.sqrt(sum((p - q) ** 2 for p, q in zip(target_point, nearest_list[-1].coords)))
                else:
                    max_dist = float('inf')

                distance_to_right = calc_distance_to_box(calc_bounding_box(node.rightchild), target_point)
                distance_to_left = calc_distance_to_box(calc_bounding_box(node.leftchild), target_point)

                if distance_to_left <= distance_to_right and (len(nearest_list) < num_neighbors or distance_to_left <= max_dist):
                    checked_leaves, nearest_list = search_knn(node.leftchild, checked_leaves, nearest_list, num_neighbors, target_point)
                    max_dist = math.sqrt(sum((p - q) ** 2 for p, q in zip(target_point, nearest_list[-1].coords)))

                    if len(nearest_list) < num_neighbors or distance_to_right <= max_dist:
                        checked_leaves, nearest_list = search_knn(node.rightchild, checked_leaves, nearest_list, num_neighbors, target_point)

                elif distance_to_right < distance_to_left and (len(nearest_list) < num_neighbors or distance_to_right <= max_dist):
                    checked_leaves, nearest_list = search_knn(node.rightchild, checked_leaves, nearest_list, num_neighbors, target_point)
                    max_dist = math.sqrt(sum((p - q) ** 2 for p, q in zip(target_point, nearest_list[-1].coords)))

                    if len(nearest_list) < num_neighbors or distance_to_left <= max_dist:
                        checked_leaves, nearest_list = search_knn(node.leftchild, checked_leaves, nearest_list, num_neighbors, target_point)

                return checked_leaves, nearest_list

            elif isinstance(node, NodeLeaf):
                    all_candidates = sorted(node.data + nearest_list, key=lambda datum: (math.sqrt(sum((coord - point_coord) ** 2 for coord, point_coord in zip(datum.coords, target_point))), datum.code))
                    all_candidates = all_candidates[:min(num_neighbors, len(all_candidates))]

                    return checked_leaves + 1, all_candidates

        def calc_distance_to_box(box, point):
            return math.sqrt(sum((max(interval[0], min(val, interval[1])) - val) ** 2 for interval, val in zip(box, point)))

        checked_leaves, nearest_neighbors = search_knn(self.root, 0, [], k, point)

        return json.dumps({"leaveschecked": checked_leaves, "points": [datum.to_json() for datum in nearest_neighbors]}, indent=2)