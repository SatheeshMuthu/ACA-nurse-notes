# extract_notes.py
import requests
import json


# change BASE_URL to your deployed app or host IP
BASE_URL = "http://127.0.0.1:8000" # or "http://192.168.1.74:8000" or https://<your-fqdn>


def fetch_all_notes():
    r = requests.get(f"{BASE_URL}/api/v1/notes", timeout=10)
    r.raise_for_status()
    return r.json()


def fetch_single(note_id):
    r = requests.get(f"{BASE_URL}/api/v1/notes/{note_id}", timeout=10)
    r.raise_for_status()
    return r.json()


if __name__ == "__main__":
    notes = fetch_all_notes()
    print(f"Retrieved {len(notes)} notes")
    for n in notes:
        print(n['id'], n['note_date'], n['text'][:80])
    # save to file
    with open('nurse_notes.json', 'w', encoding='utf-8') as f:
        json.dump(notes, f, indent=2, ensure_ascii=False)
    print('Saved nurse_notes.json')


    # fetch single
    single = fetch_single('note-1')
    print('\nSingle note:\n', single)