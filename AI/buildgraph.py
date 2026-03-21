import json
import networkx as nx

def build_curriculum_graph(course_catalog):
    G = nx.DiGraph()
    for course, data in course_catalog.items():
        G.add_node(course, type=data.get('type', 'technical'))
        for prereq in data.get('prerequisites', []):
            G.add_edge(prereq, course)
    return G

def generate_training_roadmap(skill_gap, G, skill_to_course_map):

    required_courses = set()
    for skill in skill_gap:
        course = skill_to_course_map.get(skill.lower())
        if course:
            required_courses.add(course)
            required_courses.update(nx.ancestors(G, course))
            

    subgraph = G.subgraph(required_courses)
    try:

        pathway = list(nx.topological_sort(subgraph))
        return pathway
    except nx.NetworkXUnfeasible:
        return "Error: Circular dependency in curriculum."

catalog = {
    "Python 101": {"prerequisites": [], "type": "core"},
    "Data Analysis": {"prerequisites": ["Python 101"], "type": "technical"},
    "Machine Learning": {"prerequisites": ["Data Analysis"], "type": "advanced"},
    "Corporate Compliance": {"prerequisites": [], "type": "soft-skill"}
}

skill_map = {
    "python": "Python 101",
    "statistics": "Data Analysis",
    "regression": "Machine Learning",
    "integrity": "Corporate Compliance"
}

G = build_curriculum_graph(catalog)


with open("./AI/processedD.json", "r") as f:
    data = json.load(f)
    sample_gap = data[0]['skill_gap']

pathway = generate_training_roadmap(sample_gap, G, skill_map)
print(f"Optimal Learning Pathway: {pathway}")