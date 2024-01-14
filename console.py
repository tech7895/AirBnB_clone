#!/usr/bin/python3
"""The script defines the HBnB console"""
import re
import cmd
from shlex import split
from models import storage
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.place import Place
from models.amenity import Amenity
from models.review import Review


def parse(arg):
    curly_bracesMatch = re.search(r"\{(.*?)\}", arg)
    brackets = re.search(r"\[(.*?)\]", arg)
    if curly_bracesMatch is None:
        if brackets is None:
            return [i.strip(",") for i in split(arg)]
        else:
            lexer = split(arg[:brackets.span()[0]])
            result_lst = [i.strip(",") for i in lexer]
            result_lst.append(brackets.group())
            return result_lst
    else:
        lexer = split(arg[:curly_bracesMatch.span()[0]])
        result_lst = [i.strip(",") for i in lexer]
        result_lst.append(curly_bracesMatch.group())
        return result_lst


class my_command(cmd.Cmd):
    """The script defines the HBnB command
    interpreter.

    Attributes:
        prompt (str): the command prompt
    """

    prompt = "(hbnb) "
    __classes = {
        "BaseModel",
        "User",
        "State",
        "City",
        "Place",
        "Amenity",
        "Review"
    }

    def emptyline(self):
        """This does nothing upon receiving an empty line."""
        pass

    def default(self, arg):
        """A default behavior for cmd module when input
        is invalid"""
        argdict = {
            "all": self.do_all,
            "show": self.do_show,
            "destroy": self.make_destroy,
            "count": self.do_count,
            "update": self.do_update
        }
        match = re.search(r"\.", arg)
        if match is not None:
            args_lst = [arg[:match.span()[0]], arg[match.span()[1]:]]
            match = re.search(r"\((.*?)\)", args_lst[1])
            if match is not None:
                command = [args_lst[1][:match.span()[0]], match.group()[1:-1]]
                if command[0] in argdict.keys():
                    call = "{} {}".format(args_lst[0], command[1])
                    return argdict[command[0]](call)
        print("*** Unknown syntax: {}".format(arg))
        return False

    def do_quit(self, arg):
        """This quits command to exit the program."""
        return True

    def do_EOF(self, arg):
        """The EOF signal to exit the program."""
        print("")
        return True

    def do_create(self, arg):
        """Usage: create <class>
        Creates a new class instance and print its id.
        """
        args_lst = parse(arg)
        if len(args_lst) == 0:
            print("** class name missing **")
        elif args_lst[0] not in my_command.__classes:
            print("** class doesn't exist **")
        else:
            print(eval(args_lst[0])().id)
            storage.save()

    def do_show(self, arg):
        """Usage: show <class> <id> or <class>.show(<id>)
        Displays the string representation of a class instance of
        a given id.
        """
        args_lst = parse(arg)
        obj_dict = storage.all()
        if len(args_lst) == 0:
            print("** class name missing **")
        elif args_lst[0] not in my_command.__classes:
            print("** class doesn't exist **")
        elif len(args_lst) == 1:
            print("** instance id missing **")
        elif "{}.{}".format(args_lst[0], args_lst[1]) not in obj_dict:
            print("** no instance found **")
        else:
            print(obj_dict["{}.{}".format(args_lst[0], args_lst[1])])

    def make_destroy(self, arg):
        """Usage: destroy <class> <id> or <class>.destroy(<id>)
        Deletes a class instance of a given id."""
        args_lst = parse(arg)
        obj_dict = storage.all()
        if len(args_lst) == 0:
            print("** class name missing **")
        elif args_lst[0] not in my_command.__classes:
            print("** class doesn't exist **")
        elif len(args_lst) == 1:
            print("** instance id missing **")
        elif "{}.{}".format(args_lst[0], args_lst[1]) not in obj_dict.keys():
            print("** no instance found **")
        else:
            del obj_dict["{}.{}".format(args_lst[0], args_lst[1])]
            storage.save()

    def do_all(self, arg):
        """Usage: all or all <class> or <class>.all()
        Displays a string representations of all instances of a given class.
        If no class is specified, displays all instantiated objects."""
        args_lst = parse(arg)
        if len(args_lst) > 0 and args_lst[0] not in my_command.__classes:
            print("** class doesn't exist **")
        else:
            result_lst = []
            for obj in storage.all().values():
                if len(args_lst) > 0 and args_lst[0] == obj.__class__.__name__:
                    result_lst.append(obj.__str__())
                elif len(args_lst) == 0:
                    result_lst.append(obj.__str__())
            print(result_lst)

    def do_count(self, arg):
        """Usage: count <class> or <class>.count()
        Retrieves the number of instances of a given class."""
        args_lst = parse(arg)
        count = 0
        for obj in storage.all().values():
            if args_lst[0] == obj.__class__.__name__:
                count += 1
        print(count)

    def do_update(self, arg):
        """Usage: update <class> <id> <attribute_name> <attribute_value> or
       <class>.update(<id>, <attribute_name>, <attribute_value>) or
       <class>.update(<id>, <dictionary>)
        Updates a class instance of a given id by adding or updating
        a given attribute key/value pair or dictionary."""
        args_lst = parse(arg)
        obj_dict = storage.all()

        if len(args_lst) == 0:
            print("** class name missing **")
            return False
        if args_lst[0] not in my_command.__classes:
            print("** class doesn't exist **")
            return False
        if len(args_lst) == 1:
            print("** instance id missing **")
            return False
        if "{}.{}".format(args_lst[0], args_lst[1]) not in obj_dict.keys():
            print("** no instance found **")
            return False
        if len(args_lst) == 2:
            print("** attribute name missing **")
            return False
        if len(args_lst) == 3:
            try:
                type(eval(args_lst[2])) != dict
            except NameError:
                print("** value missing **")
                return False

        if len(args_lst) == 4:
            obj = obj_dict["{}.{}".format(args_lst[0], args_lst[1])]
            if args_lst[2] in obj.__class__.__dict__.keys():
                valtype = type(obj.__class__.__dict__[args_lst[2]])
                obj.__dict__[args_lst[2]] = valtype(args_lst[3])
            else:
                obj.__dict__[args_lst[2]] = args_lst[3]
        elif type(eval(args_lst[2])) == dict:
            obj = obj_dict["{}.{}".format(args_lst[0], args_lst[1])]
            for k, v in eval(args_lst[2]).items():
                if (k in obj.__class__.__dict__.keys() and
                        type(obj.__class__.__dict__[k]) in {str, int, float}):
                    valtype = type(obj.__class__.__dict__[k])
                    obj.__dict__[k] = valtype(v)
                else:
                    obj.__dict__[k] = v
        storage.save()


if __name__ == "__main__":
    my_command().cmdloop()
