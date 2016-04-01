#! /usr/bin/python
"""Module for creating a command line notebook app."""
import datetime, sys

class Menu(object):
    """Menu with options to interact with the notebook."""
    def __init__(self):
        self.notebook = Notebook()

    def display_menu(self):
        print """ Notebook Menu

        [1] show [note_id] (If no id is given, shows all notes)
        [2] search [filter] (Searches all notes by filter)
        [3] add (Adds note)
        [4] modify <note_id> (Adds/deletes memo or tags)
        [5] delete <note_id> (Deletes note)
        [6] quit (Exits the notebook app)"""

    def run(self):
        while True:
            self.display_menu()
            choice = raw_input("Enter an option: ")
            command = choice.split(" ")
            if command[0] == "show":
                if len(command) > 1:
                    if command[1][:].isdigit() and \
                        int(command[1]) < self.notebook.next_id:
                        self.show_notes(int(command[1]))
                    else:
                        print "The note id is not valid."
                else:
                    self.show_notes()

            elif command[0] == "search":
                if len(command) > 1:
                    self.search_notes(command[1])
                else:
                    self.search_notes()

            elif command[0] == "add":
                self.add_note()

            elif command[0] == "modify":
                if len(command) > 1 and command[1][:].isdigit() and \
                    int(command[1]) < self.notebook.next_id:
                    self.modify_note(int(command[1]))
                else:
                    print "This command requires a (valid) note id."

            elif command[0] == "delete":
                if len(command) > 1 and command[1][:].isdigit():
                    self.delete_note(int(command[1]))
                else:
                    print "This command requires a (valid) note id."

            elif command[0] == "quit":
                self.quit()

            else:
                print "Invalid command"

    def show_notes(self, note_id=None, notes=None):
        if not notes:
            notes = self.notebook.notes
        for note in notes:
            if note_id == None or note.id == note_id:
                print note

    def search_notes(self, search_filter=""):
        notes = self.notebook.search(search_filter)
        self.show_notes(notes=notes)

    def add_note(self):
        memo = raw_input("Enter a memo: ")
        tags_string = raw_input("Enter tags separated by commas: ")
        tags = tags_string.split(',')
        self.notebook.add_note(memo, tags)

    def delete_note(self, note_id):
        self.notebook.delete_note(note_id)

    def modify_note(self, note_id):
        print "If option doesn't apply, press ENTER.\n"
        memo_to_add = raw_input("Enter a memo (will erase the old one): ")
        memo_to_continue = raw_input("Continue the old memo with: ")
        tag_to_add = raw_input("Add tag: ")
        tag_to_delete = raw_input("Delete tag: ")
        if memo_to_add:
            self.notebook.rewrite_memo(note_id, memo_to_add)
        if memo_to_continue:
            self.notebook.continue_memo(note_id, memo_to_continue)
        if tag_to_add:
            self.notebook.add_tag(note_id, tag_to_add)
        if tag_to_delete:
            self.notebook.remove_tag(note_id, tag_to_delete)


    def quit(self):
        print "Closing notebook..."
        sys.exit(0)


class Notebook(object):
    """Collection of notes that can be modified."""
    def __init__(self):
        self.notes = []
        self.next_id = 0

    def add_note(self, memo, tags=[]):
        self.notes.append(Note(memo, self.next_id, tags))
        self.next_id += 1

    def rewrite_memo(self, note_id, memo):
        found = False
        for note in self.notes:
            if note.id == note_id:
                note.memo = memo
                found = True
                break
        if not found:
            print "Note with id %d doesn't exist." % (note_id)

    def continue_memo(self, note_id, memo):
        found = False
        for note in self.notes:
            if note.id == note_id:
                note.memo = note.memo + "\n" + memo
                found = True
                break
        if not found:
            print "Note with id %d doesn't exist." % (note_id)

    def remove_tag(self, note_id, tag_to_remove):
        found = False
        for note in self.notes:
            if note.id == note_id:
                note.tags[:] = [tag for tag in note.tags \
                    if tag != tag_to_remove]
                found = True
                break
        if not found:
            print "Note with id %d doesn't exist." % (note_id)

    def add_tag(self, note_id, tag):
        found = False
        for note in self.notes:
            if note.id == note_id:
                note.tags.append(tag)
                found = True
                break
        if not found:
            print "Note with id %d doesn't exist." % (note_id)

    def delete_note(self, note_id):
        self.notes[:] = [note for note in self.notes if note.id != note_id]

    def search(self, search_filter):
        return [note for note in self.notes if note.match(search_filter)]


class Note(object):
    """Has a memo, a list of tags, an id and a creation date."""
    def __init__(self, memo, next_id, tags=[]):
        self.memo = memo
        self.tags = tags
        self.creation_date = datetime.date.today()
        self.id = next_id

    def match(self, match_filter):
        """Test if the filter matches the memo or the tags."""
        return match_filter in self.memo or match_filter in self.tags

    def __str__(self):
        tags = ""
        for tag in self.tags:
            tags += tag + ", "
        tags = tags[:-2]
        return "\n" + "Entry number: %d\n" % (self.id) + \
        "Date: %s\n" % (self.creation_date) + "-" * 20 + \
        "\n" + self.memo +"\n" + "-" * 20 + "\n" + "Tags: " + \
        tags + "\n"
