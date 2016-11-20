import yaml
import os
import inspect

class Ship:
    def __init__(self, name, *args):
        self.name = name
        for arg in args:
            if isinstance(arg, dict):
                (argname, value) = arg.popitem()
                setattr(self, argname, value)
            else:
                setattr(self, arg, True)
    def is_authorized(self, criteria):
        if hasattr(self, criteria) and getattr(self, criteria) is not False:
            return True
        else:
            return False
    def restriction(self, criteria):
        if self.is_authorized(criteria) and getattr(self, criteria) is not True:
            return getattr(self, criteria)
        else:
            return ""
    def print_if_authorized(self, era, squad=None):
        if self.is_authorized(era):
            if squad is not None and self.is_authorized(squad):
                print(self.name + (", %s" % self.restriction(era) if self.restriction(era) is not "" else "")
                      + (", %s" % self.restriction(squad) if self.restriction(squad) is not "" else ""))
            else:
                print(self.name + (", %s" % self.restriction(era) if self.restriction(era) is not "" else ""))
                    
    def __repr__(self):
        return "%s(%s, " % (self.__class__.__name__, self.name) + ", ".join(["%s: %s" % (var, getattr(self, var)) for var in vars(self) if var is not "name"]) + ")"

def print_list(ships, era, squad=None):
    print("** %s" % era + (" %s" % squad if squad is not None else "") + " ships:")
    for ship in ships:
        ship.print_if_authorized(era, squad)
    print("")

if __name__=='__main__':
    this_file = os.path.abspath(inspect.getfile(inspect.currentframe()))
    project_dir = os.path.dirname(os.path.dirname(os.path.dirname(this_file)))
    with open(os.path.join(project_dir, 'data', 'scum_ships.yml'), 'r') as f:
        data = yaml.load(f)
        ships = [Ship(name, *parameters) for name, parameters in sorted(data.items())]
        print_list(ships, 'Rebellion', 'Superiority')
        print_list(ships, 'New Order')
