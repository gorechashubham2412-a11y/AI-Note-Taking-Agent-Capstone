"""
AI Note-providing Agent From Text - Google 5-Day AI Agentic Program Capstone Project
Features: Tool Use, Memory, and Evaluation
"""

import os
import json
from datetime import datetime
from pathlib import Path
import google.generativeai as genai

# Configuration
genai.configure(api_key="AIzaSyDBCI94TUcyGYbdH5rfJpREz0l6RnzUFPE")
model = genai.GenerativeModel('gemini-2.5-flash')

class NoteMemory:
    """Memory System: Stores user preferences and session history"""
    def __init__(self, memory_file="agent_memory.json"):
        self.memory_file = memory_file
        self.memory = self._load_memory()
    
    def _load_memory(self):
        if Path(self.memory_file).exists():
            with open(self.memory_file, 'r') as f:
                return json.load(f)
        return {
            "preferences": {"style": "detailed", "format": "bullet"},
            "sessions": []
        }
    
    def save_session(self, audio_file, notes, quality_score):
        session = {
            "timestamp": datetime.now().isoformat(),
            "audio_file": audio_file,
            "notes_preview": notes[:100],
            "quality_score": quality_score
        }
        self.memory["sessions"].append(session)
        self._save_memory()
    
    def update_preference(self, key, value):
        self.memory["preferences"][key] = value
        self._save_memory()
    
    def get_preference(self, key):
        return self.memory["preferences"].get(key, "detailed")
    
    def _save_memory(self):
        with open(self.memory_file, 'w') as f:
            json.dump(self.memory, f, indent=2)
    
    def get_history_summary(self):
        return f"Total sessions: {len(self.memory['sessions'])}"


class NoteEvaluator:
    """Evaluation System: Assesses note quality and provides metrics"""
    
    @staticmethod
    def evaluate_notes(transcript, notes):
        """Evaluates note quality based on key metrics"""
        scores = {}
        
        # 1. Completeness: Check if key info is captured
        transcript_words = set(transcript.lower().split())
        notes_words = set(notes.lower().split())
        common_words = transcript_words.intersection(notes_words)
        scores['completeness'] = min(len(common_words) / max(len(transcript_words), 1) * 100, 100)
        
        # 2. Conciseness: Notes should be shorter than transcript
        compression_ratio = len(notes) / max(len(transcript), 1)
        scores['conciseness'] = max(0, (1 - compression_ratio) * 100)
        
        # 3. Structure: Check for proper formatting
        has_structure = any(marker in notes for marker in ['##', '**', '-', '•', '1.'])
        scores['structure'] = 100 if has_structure else 50
        
        # Overall quality score
        overall = sum(scores.values()) / len(scores)
        
        return {
            "overall_quality": round(overall, 2),
            "metrics": {k: round(v, 2) for k, v in scores.items()},
            "feedback": NoteEvaluator._generate_feedback(scores)
        }
    
    @staticmethod
    def _generate_feedback(scores):
        feedback = []
        if scores['completeness'] < 70:
            feedback.append("Consider capturing more key points")
        if scores['conciseness'] < 50:
            feedback.append("Notes could be more concise")
        if scores['structure'] < 80:
            feedback.append("Add more structure (headers, bullets)")
        return feedback if feedback else ["Great quality notes!"]


class AudioTranscriber:
    """Tool Use #1: Transcribes audio to text"""
    
    @staticmethod
    def transcribe(audio_path):
        # Mock transcription for demo
        print("-" * 20)
        querry= input("📍 Enter your text: ")
        return querry


class NoteGenerator:
    """Tool Use #2: Generates structured notes from transcript"""
    
    def __init__(self, model, memory):
        self.model = model
        self.memory = memory
    
    def generate_notes(self, transcript):
        style = self.memory.get_preference("style")
        format_type = self.memory.get_preference("format")
        
        prompt = f"""
        Create {style} notes from this transcript in {format_type} format.
        
        Guidelines:
        - Extract key points and action items
        - Use clear structure with headers
        - Include dates, numbers, and names
        - Highlight important decisions
        - Give Important question's list
        
        Transcript:
        {transcript}
        
        Generate well-structured notes:
        """
        
        print("🤖 Generating notes with AI...")
        response = self.model.generate_content(prompt)
        return response.text


class NoteTakingAgent:
    """Main Agent: Orchestrates all components"""
    
    def __init__(self):
        self.memory = NoteMemory()
        self.transcriber = AudioTranscriber()
        self.note_generator = NoteGenerator(model, self.memory)
        self.evaluator = NoteEvaluator()
        print("✅ AI Note-Taking Agent initialized")
        print(f"📊 {self.memory.get_history_summary()}")
    
    def process_recording(self, audio_path):
        """Main agent workflow"""
        
        # Step 1: Transcribe audio (Tool Use)
        transcript = self.transcriber.transcribe(audio_path)
        print("\n" + "="*50)
        print(f"✓ Transcription complete ({len(transcript)} chars)")
        
        # Step 2: Generate notes (Tool Use + Memory)
        notes = self.note_generator.generate_notes(transcript)
        print(f"✓ Notes generated ({len(notes)} chars)")
        
        # Step 3: Evaluate quality (Evaluation)
        evaluation = self.evaluator.evaluate_notes(transcript, notes)
        print(f"✓ Quality score: {evaluation['overall_quality']}/100")
        
        # Step 4: Save to memory (Memory)
        self.memory.save_session(audio_path, notes, evaluation['overall_quality'])
        
        return {
            "transcript": transcript,
            "notes": notes,
            "evaluation": evaluation
        }
    
    def set_preference(self, style=None, format_type=None):
        """Update user preferences"""
        if style:
            self.memory.update_preference("style", style)
            print(f"✓ Style preference updated to: {style}")
        if format_type:
            self.memory.update_preference("format", format_type)
            print(f"✓ Format preference updated to: {format_type}")
    
    def export_notes(self, notes, output_path="notes_output.md"):
        """Tool Use #3: Export notes to file"""
        with open(output_path, 'w') as f:
            f.write(f"# Meeting Notes\n")
            f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n")
            f.write(notes)
        print(f"✓ Notes exported to: {output_path}")


# Demo Usage
def main():
    # Initialize agent
    agent = NoteTakingAgent()
    
    # Process a recording
    result = agent.process_recording("meeting_recording.mp3")
    
    # Display results
    print("\n" + "="*50)
    print("📋 GENERATED NOTES:")
    print("="*50)
    print(result['notes'])
    
    print("\n" + "="*50)
    print("📊 EVALUATION REPORT:")
    print("="*50)
    print(f"Overall Quality: {result['evaluation']['overall_quality']}/100")
    print(f"Metrics: {result['evaluation']['metrics']}")
    print(f"Feedback: {', '.join(result['evaluation']['feedback'])}")
    
    # Export notes
    agent.export_notes(result['notes'])
    
    # Demonstrate memory: Change preferences
    print("\n" + "="*50)
    print("🔧 UPDATING PREFERENCES:")
    print("="*50)
    agent.set_preference(style="brief", format_type="numbered")
    
    print("\n✅ Agent demonstration complete!")
    print("📁 Check 'notes_output.md' and 'agent_memory.json'")


if __name__ == "__main__":
    main()