from flask import Flask, jsonify, request, session, redirect, url_for,Blueprint,render_template as render
import subprocess
from .connection import connection


bot_routes =Blueprint('bot', __name__)

@bot_routes.route('/ollama-chat', methods=['POST'])
def ollama_chat():
    try:
        prompt = request.json.get('prompt')
      
        process = subprocess.Popen(
            ['ollama', 'run', 'qwen2:1.5b'], 
            stdin=subprocess.PIPE, 
            stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE,
            text=True
        )
        
        
        stdout, stderr = process.communicate(input=prompt)
        
        if process.returncode != 0:
            return jsonify({"error": f"Error: {stderr}"}), 500
        
        return jsonify({"response": stdout})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


