import streamlit as st
import random
import time

# Custom CSS for a cool, modern look
st.markdown("""
    <style>
    .main {
        background-color: #1e1e2f;
        color: #ffffff;
        font-family: 'Arial', sans-serif;
    }
    .stButton>button {
        background-color: #00d4ff;
        color: black;
        border-radius: 10px;
        font-weight: bold;
        padding: 10px 20px;
        transition: all 0.3s;
    }
    .stButton>button:hover {
        background-color: #ff007a;
        color: white;
    }
    .stProgress .st-bo {
        background-color: #00d4ff;
    }
    .title {
        font-size: 40px;
        color: #00d4ff;
        text-align: center;
        text-transform: uppercase;
        letter-spacing: 2px;
    }
    .subtitle {
        font-size: 20px;
        color: #ff007a;
        text-align: center;
        margin-bottom: 20px;
    }
    .question-text {
        font-size: 18px;
        margin-bottom: 10px;
    }
    .result-box {
        background-color: #2d2d44;
        padding: 15px;
        border-radius: 10px;
        margin-bottom: 10px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
    }
    .stRadio>label {
        color: #ffffff;
        font-size: 16px;
    }
    </style>
""", unsafe_allow_html=True)

# Define total_time globally
TOTAL_TIME = 600  # 10 minutes in seconds

# Full question bank with 100 questions
questions = [
    # Algorithms (20 Questions)
    {"question": "What is the average time complexity of QuickSort?", "options": ["O(n)", "O(n log n)", "O(n²)", "O(log n)"], "answer": "O(n log n)"},
    {"question": "Which sorting algorithm uses Divide and Conquer?", "options": ["Bubble Sort", "Merge Sort", "Selection Sort", "Insertion Sort"], "answer": "Merge Sort"},
    {"question": "What is the worst-case time complexity of Merge Sort?", "options": ["O(n)", "O(n log n)", "O(n²)", "O(log n)"], "answer": "O(n log n)"},
    {"question": "Which algorithm is used for finding the shortest path in a weighted graph with negative edges?", "options": ["Dijkstra's", "Bellman-Ford", "Floyd-Warshall", "Kruskal's"], "answer": "Bellman-Ford"},
    {"question": "Most efficient algorithm to detect a cycle in a graph?", "options": ["DFS", "BFS", "Prim's", "Kruskal's"], "answer": "DFS"},
    {"question": "Difference between graph and tree traversal includes:", "options": ["Loop in graph", "DFS uses stack", "BFS uses queue vs recursive for trees", "All of the above"], "answer": "All of the above"},
    {"question": "Appropriate data structure for BFS?", "options": ["Stack", "Queue", "Priority Queue", "Union Find"], "answer": "Queue"},
    {"question": "Which is not a stable sorting algorithm in typical implementation?", "options": ["Insertion Sort", "Merge Sort", "Quick Sort", "Bubble Sort"], "answer": "Quick Sort"},
    {"question": "Best performance sorting for almost sorted array (max 1-2 misplaced)?", "options": ["Quick Sort", "Heap Sort", "Merge Sort", "Insertion Sort"], "answer": "Insertion Sort"},
    {"question": "Time complexity of Binary Search?", "options": ["O(n)", "O(log n)", "O(n log n)", "O(n²)"], "answer": "O(log n)"},
    {"question": "Which algorithm is used for finding Strongly Connected Components?", "options": ["Kosaraju's", "Dijkstra's", "Prim's", "Kruskal's"], "answer": "Kosaraju's"},
    {"question": "What is the time complexity of Kruskal's algorithm?", "options": ["O(E log V)", "O(V log V)", "O(E)", "O(V²)"], "answer": "O(E log V)"},
    {"question": "Which algorithm is best for sorting when memory is limited?", "options": ["Quick Sort", "Merge Sort", "Heap Sort", "Bubble Sort"], "answer": "Heap Sort"},
    {"question": "What is the space complexity of Depth-First Search?", "options": ["O(V)", "O(E)", "O(V + E)", "O(log V)"], "answer": "O(V)"},
    {"question": "Which sorting algorithm has the best average-case time complexity?", "options": ["Quick Sort", "Merge Sort", "Heap Sort", "Insertion Sort"], "answer": "Quick Sort"},
    {"question": "What is the recurrence relation for QuickSort?", "options": ["T(n) = T(n-1) + O(n)", "T(n) = 2T(n/2) + O(n)", "T(n) = T(n/2) + O(n log n)", "T(n) = T(n/10) + T(9n/10) + O(n)"], "answer": "T(n) = 2T(n/2) + O(n)"},
    {"question": "Which algorithm is used for topological sorting?", "options": ["DFS", "BFS", "Kahn's", "Prim's"], "answer": "Kahn's"},
    {"question": "What is the time complexity of Floyd-Warshall algorithm?", "options": ["O(V)", "O(V log V)", "O(V²)", "O(V³)"], "answer": "O(V³)"},
    {"question": "Which algorithm is non-comparison based?", "options": ["Quick Sort", "Merge Sort", "Radix Sort", "Heap Sort"], "answer": "Radix Sort"},
    {"question": "What is the best-case time complexity of Bubble Sort?", "options": ["O(n)", "O(n log n)", "O(n²)", "O(log n)"], "answer": "O(n)"},

    # Data Structures (20 Questions)
    {"question": "Which data structure follows the LIFO principle?", "options": ["Queue", "Stack", "Array", "Tree"], "answer": "Stack"},
    {"question": "Which type of linked list allows traversal in both directions?", "options": ["Singly Linked List", "Doubly Linked List", "Circular Linked List", "Array"], "answer": "Doubly Linked List"},
    {"question": "What is the time complexity of accessing an element in an array?", "options": ["O(1)", "O(log n)", "O(n)", "O(n log n)"], "answer": "O(1)"},
    {"question": "Which data structure is best for implementing a priority queue?", "options": ["Array", "Linked List", "Heap", "Stack"], "answer": "Heap"},
    {"question": "What is the space complexity of a binary search tree?", "options": ["O(n)", "O(log n)", "O(n log n)", "O(1)"], "answer": "O(n)"},
    {"question": "Which operation is slowest in a linked list?", "options": ["Access", "Insert", "Delete", "Search"], "answer": "Access"},
    {"question": "What is the maximum number of children in a binary tree node?", "options": ["1", "2", "3", "4"], "answer": "2"},
    {"question": "Which data structure uses FIFO principle?", "options": ["Stack", "Queue", "Deque", "Heap"], "answer": "Queue"},
    {"question": "What is the time complexity of inserting at the beginning of a linked list?", "options": ["O(1)", "O(log n)", "O(n)", "O(n log n)"], "answer": "O(1)"},
    {"question": "Which traversal of a binary tree visits root first?", "options": ["Preorder", "Inorder", "Postorder", "Level Order"], "answer": "Preorder"},
    {"question": "What is the worst-case time complexity of searching in a hash table?", "options": ["O(1)", "O(log n)", "O(n)", "O(n log n)"], "answer": "O(n)"},
    {"question": "Which data structure is used for implementing recursion?", "options": ["Stack", "Queue", "Array", "Linked List"], "answer": "Stack"},
    {"question": "What is the time complexity of deleting the last element in a singly linked list?", "options": ["O(1)", "O(log n)", "O(n)", "O(n log n)"], "answer": "O(n)"},
    {"question": "Which sorting algorithm is in-place and stable?", "options": ["Quick Sort", "Merge Sort", "Insertion Sort", "Heap Sort"], "answer": "Insertion Sort"},
    {"question": "What is the maximum height of a binary heap with n nodes?", "options": ["log n", "n", "n log n", "n²"], "answer": "log n"},
    {"question": "Which data structure is used for implementing a graph?", "options": ["Array", "Linked List", "Adjacency Matrix", "Adjacency List"], "answer": "Adjacency List"},
    {"question": "What is the time complexity of enqueue operation in a queue?", "options": ["O(1)", "O(log n)", "O(n)", "O(n log n)"], "answer": "O(1)"},
    {"question": "Which traversal visits all nodes at each level before moving to the next?", "options": ["Preorder", "Inorder", "Postorder", "Level Order"], "answer": "Level Order"},
    {"question": "What is the space complexity of a queue implemented using an array?", "options": ["O(n)", "O(log n)", "O(1)", "O(n log n)"], "answer": "O(n)"},
    {"question": "Which data structure is best for implementing a set?", "options": ["Array", "Linked List", "Hash Table", "Stack"], "answer": "Hash Table"},

    # Databases (20 Questions)
    {"question": "What does SQL stand for?", "options": ["Structured Query Language", "Simple Query Logic", "System Query Language", "Structured Quick Language"], "answer": "Structured Query Language"},
    {"question": "What is the primary key in a database?", "options": ["Unique identifier", "Foreign key", "Index", "Duplicate key"], "answer": "Unique identifier"},
    {"question": "Which normal form eliminates transitive dependencies?", "options": ["1NF", "2NF", "3NF", "BCNF"], "answer": "3NF"},
    {"question": "What is the purpose of a foreign key?", "options": ["Ensure data integrity", "Speed up queries", "Store metadata", "Define primary key"], "answer": "Ensure data integrity"},
    {"question": "Which SQL command is used to retrieve data?", "options": ["INSERT", "SELECT", "UPDATE", "DELETE"], "answer": "SELECT"},
    {"question": "What is the time complexity of a linear search in a database table?", "options": ["O(1)", "O(log n)", "O(n)", "O(n log n)"], "answer": "O(n)"},
    {"question": "Which database model is based on a tree structure?", "options": ["Relational", "Hierarchical", "Network", "Object-Oriented"], "answer": "Hierarchical"},
    {"question": "What is the role of a database administrator?", "options": ["Write queries", "Manage users", "Design hardware", "Develop applications"], "answer": "Manage users"},
    {"question": "Which index is best for range queries?", "options": ["B-Tree", "Hash", "Bitmap", "Full-Text"], "answer": "B-Tree"},
    {"question": "What is ACID in database transactions?", "options": ["Atomicity, Consistency, Isolation, Durability", "Access, Control, Integrity, Data", "Accuracy, Consistency, Isolation, Durability", "Atomicity, Control, Integrity, Data"], "answer": "Atomicity, Consistency, Isolation, Durability"},
    {"question": "Which SQL clause is used for sorting results?", "options": ["WHERE", "GROUP BY", "ORDER BY", "HAVING"], "answer": "ORDER BY"},
    {"question": "What is the purpose of normalization?", "options": ["Reduce redundancy", "Increase storage", "Speed up queries", "Simplify joins"], "answer": "Reduce redundancy"},
    {"question": "Which type of join returns all records when there is a match?", "options": ["INNER JOIN", "LEFT JOIN", "RIGHT JOIN", "FULL JOIN"], "answer": "INNER JOIN"},
    {"question": "What is the time complexity of a B-Tree search?", "options": ["O(1)", "O(log n)", "O(n)", "O(n log n)"], "answer": "O(log n)"},
    {"question": "Which database is best for unstructured data?", "options": ["MySQL", "MongoDB", "Oracle", "PostgreSQL"], "answer": "MongoDB"},
    {"question": "What is a view in SQL?", "options": ["Virtual table", "Stored procedure", "Trigger", "Index"], "answer": "Virtual table"},
    {"question": "Which SQL command is used to add new records?", "options": ["INSERT", "UPDATE", "DELETE", "SELECT"], "answer": "INSERT"},
    {"question": "What is the purpose of a trigger in a database?", "options": ["Automate tasks", "Speed up queries", "Store data", "Define keys"], "answer": "Automate tasks"},
    {"question": "Which normal form deals with multivalued dependencies?", "options": ["2NF", "3NF", "BCNF", "4NF"], "answer": "4NF"},
    {"question": "What is the role of a transaction log?", "options": ["Track changes", "Speed up queries", "Store metadata", "Define relationships"], "answer": "Track changes"},

    # Operating Systems (20 Questions)
    {"question": "What is a deadlock in an operating system?", "options": ["Infinite loop", "Memory overflow", "Resource contention", "Process termination"], "answer": "Resource contention"},
    {"question": "Which scheduling algorithm is preemptive?", "options": ["FCFS", "SJF", "Round Robin", "Priority"], "answer": "Round Robin"},
    {"question": "What is the purpose of virtual memory?", "options": ["Extend physical memory", "Improve security", "Speed up processes", "Manage files"], "answer": "Extend physical memory"},
    {"question": "Which scheduling is non-preemptive?", "options": ["FCFS", "Round Robin", "Priority", "Multilevel"], "answer": "FCFS"},
    {"question": "What is the role of the kernel in an OS?", "options": ["Manage hardware", "Run applications", "Store data", "Define networks"], "answer": "Manage hardware"},
    {"question": "Which memory management technique uses paging?", "options": ["Segmentation", "Paging", "Swapping", "Compaction"], "answer": "Paging"},
    {"question": "What is the time complexity of process scheduling in FCFS?", "options": ["O(1)", "O(log n)", "O(n)", "O(n log n)"], "answer": "O(1)"},
    {"question": "Which OS component handles I/O operations?", "options": ["Kernel", "Shell", "File system", "Device driver"], "answer": "Device driver"},
    {"question": "What is the purpose of a semaphore?", "options": ["Synchronize processes", "Manage memory", "Speed up I/O", "Define networks"], "answer": "Synchronize processes"},
    {"question": "Which scheduling algorithm minimizes waiting time?", "options": ["SJF", "FCFS", "Round Robin", "Priority"], "answer": "SJF"},
    {"question": "What is thrashing in OS?", "options": ["Excessive paging", "Memory overflow", "Process termination", "Disk failure"], "answer": "Excessive paging"},
    {"question": "Which file system is used in Linux?", "options": ["NTFS", "FAT32", "ext4", "HFS+"], "answer": "ext4"},
    {"question": "What is the role of a process control block?", "options": ["Store process state", "Manage memory", "Speed up I/O", "Define networks"], "answer": "Store process state"},
    {"question": "Which OS supports multitasking?", "options": ["MS-DOS", "Windows", "Linux", "Both Windows and Linux"], "answer": "Both Windows and Linux"},
    {"question": "What is the time complexity of context switching?", "options": ["O(1)", "O(log n)", "O(n)", "O(n log n)"], "answer": "O(1)"},
    {"question": "Which memory allocation strategy is first-fit?", "options": ["Best-fit", "First-fit", "Worst-fit", "Next-fit"], "answer": "First-fit"},
    {"question": "What is the purpose of a deadlock prevention algorithm?", "options": ["Avoid resource contention", "Speed up processes", "Manage memory", "Define networks"], "answer": "Avoid resource contention"},
    {"question": "Which OS component manages file access?", "options": ["Kernel", "Shell", "File system", "Device driver"], "answer": "File system"},
    {"question": "What is the role of a thread in OS?", "options": ["Lightweight process", "Heavy process", "Memory unit", "Network unit"], "answer": "Lightweight process"},
    {"question": "Which scheduling algorithm uses time slices?", "options": ["FCFS", "SJF", "Round Robin", "Priority"], "answer": "Round Robin"},

    # Networking (20 Questions)
    {"question": "Which OSI layer handles routing?", "options": ["Physical", "Data Link", "Network", "Transport"], "answer": "Network"},
    {"question": "What protocol is used to send emails?", "options": ["HTTP", "FTP", "SMTP", "TCP"], "answer": "SMTP"},
    {"question": "Which layer of OSI model is responsible for error detection?", "options": ["Physical", "Data Link", "Network", "Transport"], "answer": "Data Link"},
    {"question": "What is the purpose of DHCP?", "options": ["Dynamic IP allocation", "Static IP assignment", "File transfer", "Email sending"], "answer": "Dynamic IP allocation"},
    {"question": "Which protocol is used for file transfer?", "options": ["HTTP", "FTP", "SMTP", "TCP"], "answer": "FTP"},
    {"question": "What is the time complexity of routing table lookup in a hash table?", "options": ["O(1)", "O(log n)", "O(n)", "O(n log n)"], "answer": "O(1)"},
    {"question": "Which network topology is most reliable?", "options": ["Bus", "Star", "Ring", "Mesh"], "answer": "Mesh"},
    {"question": "What is the role of a router in a network?", "options": ["Connect networks", "Manage files", "Store data", "Define processes"], "answer": "Connect networks"},
    {"question": "Which protocol ensures reliable data transfer?", "options": ["UDP", "TCP", "ICMP", "ARP"], "answer": "TCP"},
    {"question": "What is the maximum length of an Ethernet frame?", "options": ["64 bytes", "128 bytes", "1518 bytes", "2048 bytes"], "answer": "1518 bytes"},
    {"question": "Which layer of OSI model handles data encryption?", "options": ["Presentation", "Application", "Session", "Transport"], "answer": "Presentation"},
    {"question": "What is the purpose of NAT in networking?", "options": ["Network address translation", "File transfer", "Email sending", "Process management"], "answer": "Network address translation"},
    {"question": "Which protocol is used for name resolution?", "options": ["DNS", "DHCP", "FTP", "SMTP"], "answer": "DNS"},
    {"question": "What is the time complexity of a flooding algorithm in routing?", "options": ["O(1)", "O(log n)", "O(n)", "O(n log n)"], "answer": "O(n)"},
    {"question": "Which network device operates at Layer 2?", "options": ["Router", "Switch", "Hub", "Gateway"], "answer": "Switch"},
    {"question": "What is the role of ICMP in networking?", "options": ["Error reporting", "File transfer", "Email sending", "Process management"], "answer": "Error reporting"},
    {"question": "Which topology uses a central hub?", "options": ["Bus", "Star", "Ring", "Mesh"], "answer": "Star"},
    {"question": "What is the maximum speed of Fast Ethernet?", "options": ["10 Mbps", "100 Mbps", "1 Gbps", "10 Gbps"], "answer": "100 Mbps"},
    {"question": "Which protocol is connectionless?", "options": ["TCP", "UDP", "ICMP", "ARP"], "answer": "UDP"},
    {"question": "What is the purpose of a firewall in a network?", "options": ["Security", "File transfer", "Email sending", "Process management"], "answer": "Security"},
]

# Initialize session state
if 'quiz_started' not in st.session_state:
    st.session_state.quiz_started = False
if 'selected_questions' not in st.session_state:
    st.session_state.selected_questions = []
if 'current_question' not in st.session_state:
    st.session_state.current_question = 0
if 'start_time' not in st.session_state:
    st.session_state.start_time = None
if 'quiz_finished' not in st.session_state:
    st.session_state.quiz_finished = False
if 'end_time' not in st.session_state:
    st.session_state.end_time = None

# Welcome page
if not st.session_state.quiz_started:
    st.markdown("<h1 class='title'>Tech Quiz</h1>", unsafe_allow_html=True)
    st.markdown("<p class='subtitle'>For 2nd Year CSE B.Tech Students<br>Test your skills with 10 random questions out of 100!<br>You have 10 minutes. Good Luck!</p>", unsafe_allow_html=True)
    if st.button("Start Quiz"):
        st.session_state.selected_questions = random.sample(questions, 10)  # Select 10 random questions
        st.session_state.start_time = time.time()
        st.session_state.quiz_started = True
        st.session_state.current_question = 0
        st.session_state.quiz_finished = False
        st.session_state.end_time = None
        st.rerun()

# Quiz in progress
elif not st.session_state.quiz_finished:
    # Timer logic
    elapsed_time = time.time() - st.session_state.start_time
    remaining_time = max(0, TOTAL_TIME - elapsed_time)
    
    if remaining_time <= 0:
        # Time's up, end the quiz
        st.session_state.end_time = time.time()
        st.session_state.quiz_finished = True
        st.rerun()
    else:
        # Display timer and progress
        st.markdown(f"<p class='subtitle'>Time Remaining: {int(remaining_time // 60)}:{int(remaining_time % 60):02d}</p>", unsafe_allow_html=True)
        st.progress((st.session_state.current_question + 1) / 10)

        # Current question
        current_q = st.session_state.selected_questions[st.session_state.current_question]
        st.markdown(f"<p class='question-text'><strong>Question {st.session_state.current_question + 1} of 10:</strong> {current_q['question']}</p>", unsafe_allow_html=True)
        selected = st.radio("Select an option:", current_q["options"], key=f"radio_{st.session_state.current_question}")

        # Navigation buttons
        col1, col2 = st.columns(2)
        with col1:
            if st.session_state.current_question > 0:
                if st.button("Previous"):
                    st.session_state.current_question -= 1
                    st.rerun()
        with col2:
            if st.session_state.current_question < 9:
                if st.button("Next"):
                    st.session_state.current_question += 1
                    st.rerun()
            else:
                if st.button("Submit"):
                    st.session_state.end_time = time.time()
                    st.session_state.quiz_finished = True
                    st.rerun()

# Results page
else:
    st.markdown("<h1 class='title'>Quiz Results</h1>", unsafe_allow_html=True)
    
    # Calculate score
    answers = [st.session_state.get(f"radio_{i}", None) for i in range(10)]
    correct_answers = [q["answer"] for q in st.session_state.selected_questions]
    score = sum(a == c for a, c in zip(answers, correct_answers) if a is not None)
    
    # Calculate time taken
    time_taken = st.session_state.end_time - st.session_state.start_time
    minutes, seconds = divmod(int(time_taken), 60)
    result_message = "Time's up! Here are your results:" if time_taken >= TOTAL_TIME else "Quiz completed! Here are your results:"
    st.markdown(f"<p class='subtitle'>{result_message}<br>You scored {score} out of 10 in {minutes} minutes and {seconds} seconds.</p>", unsafe_allow_html=True)
    
    # Detailed feedback
    for i, q in enumerate(st.session_state.selected_questions):
        user_answer = answers[i] if answers[i] is not None else "Not answered"
        correct_answer = q["answer"]
        color = "green" if user_answer == correct_answer else "red" if user_answer != "Not answered" else "gray"
        st.markdown(
            f"<div class='result-box'>"
            f"<strong>Question {i+1}:</strong> {q['question']}<br>"
            f"Your answer: <span style='color:{color}'>{user_answer}</span><br>"
            f"Correct answer: <span style='color:green'>{correct_answer}</span>"
            f"</div>",
            unsafe_allow_html=True
        )
    
    # Retake option
    if st.button("Retake Quiz"):
        st.session_state.quiz_started = False
        st.session_state.selected_questions = []
        st.session_state.current_question = 0
        st.session_state.start_time = None
        st.session_state.end_time = None
        st.session_state.quiz_finished = False
        st.rerun()
