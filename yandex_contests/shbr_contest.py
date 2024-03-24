class Node:
    def __init__(self, data):
        self.data = data
        self.prev = None
        self.next = None


class DoublyLinkedList:
    def __init__(self):
        self.head = None

    def append(self, data):
        new_node = Node(data)
        if self.head is None:
            self.head = new_node
            return
        last_node = self.head
        while last_node.next:
            last_node = last_node.next
        last_node.next = new_node
        new_node.prev = last_node

    def print_list(self) -> str:
        result = ""
        current_node = self.head
        while current_node:
            result += current_node.data
            current_node = current_node.next
        return result


correct = input()
st = input()
command = None
com_flag = False
text: list[str] = list()
index = -1
linked_text = Node(None)
for i in range(len(st)):
    elem = st[i]
    if elem == "<":
        com_flag = True
    elif elem == ">" and com_flag:
        com_flag = False
        print(linked_text.data)
        if command == "delete":
            if linked_text.next is not None:
                print("here1")
                linked_text.next = linked_text.next.next
        elif command == "bspace":
            if linked_text.prev is not None:
                print("here2")
                new_head = linked_text.prev
                new_head.next = new_head.next.next
                new_head.next.prev = new_head
                linked_text = new_head
        elif command == "left":
            if linked_text.prev is not None:
                print("here3")
                linked_text = linked_text.prev
        elif command == "right":
            if linked_text.next is not None:
                print("here4")
                linked_text = linked_text.next
        command = None
        print(linked_text.data)
        print()
    else:
        if com_flag:
            if command is None:
                command = ""
            command += elem
        else:
            if linked_text.data is None:
                linked_text.data = elem
            else:
                if linked_text.next is None:
                    new_elem = Node(elem)
                    new_elem.prev = linked_text
                    linked_text.next = new_elem
                    linked_text = linked_text.next
                else:
                    new_elem = Node(elem)
                    new_elem.prev = linked_text
                    new_elem.next = linked_text.next
                    linked_text.next.prev = new_elem
                    linked_text.next = new_elem
                    linked_text = new_elem

text = ""
while linked_text.prev is not None:
    linked_text = linked_text.prev
while linked_text:
    text += linked_text.data
    linked_text = linked_text.next
print(text)
if "".join(text).lower() == correct.lower():
    print("Yes")
else:
    print("No")