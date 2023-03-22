from flask import Flask
from flask_restful import Resource, Api, reqparse
from flask_cors import CORS
import json
from Final_Algorithm.uF_networkAlgo import algorithm

app = Flask(__name__)
CORS(app)
api = Api(app)

parser = reqparse.RequestParser()
parser.add_argument("graph", type=str)

class TestScript(Resource):
    def post(self):
        args = parser.parse_args()
        data = json.loads(args["graph"].replace("'", '"'))
        edges = data["Edges"]
        nodes = data["Nodes"]
        root = data["Nodes"][0]
        print(edges, nodes)
        return algorithm(root, nodes=nodes, adjList=edges)
    
    

api.add_resource(TestScript, '/')

if __name__ == '__main__':
    app.run(debug=True)