import sys
import matplotlib.pyplot as plt
from IPython.display import HTML, display

from _format import HTMLBuffer, HTMLWriter
from _exceptions import ContextError, _print_error

class Registery(type):
    _shared_state = {
        'registery': {},
        'stack': []
    }
    
    def __getitem__(cls, item):
         return cls.registery.get(item, None)
    
    def __setitem__(cls, item, value):
        if item in cls:
            cls.registery.pop(item)
            cls.stack.remove(item)
            
        cls.registery[item] = value
        cls.stack.append(item)
        
    def __getattr__(cls, name):
        if name in cls._shared_state:
            return cls._shared_state[name]
        else:
            return cls.__dict__[name]
        
    def __setattr__(cls, name, value):
        if name in cls._shared_state:
            cls._shared_state[name] = value
        else:
            cls.__dict__[name] = value
    
    def __contains__(cls, item):
        return item in cls.registery
    
    def _add(cls, item, value):
        cls[item].add(value)
        
    def _pop(cls):
        if cls.stack:
            name = cls.stack.pop()
            cls.registery.pop(name)
        
    def _destroy(cls):
        cls.registery = {}
        cls.stack = []
    
    @property
    def head(cls):
        if cls.stack:
            return cls.stack[0]
        
    @property
    def tail(cls):
        if cls.stack:
            return cls.stack[-1]

class ContextManager(object):
    __metaclass__ = Registery
    
    def __init__(self):
        self._name = self.__class__.__name__

    def pop(self):
        ContextManager._pop()
    
    @classmethod
    def destroy(self):
        ContextManager._destroy()

class Node(ContextManager):
    
    def __new__(cls):
        response = super(Node, cls).__new__(cls)
        for subclass in cls.__subclasses__():
            if subclass.__name__ in cls:
                response = Node.__new__(subclass)
            else:
                response = super(Node, subclass).__new__(subclass)
                break
        return response
    
    def __init__(self):
        ContextManager.__init__(self)
        ContextManager[self._name] = self
        
        
        self._parent = self.__class__.__bases__[0].__name__
        self._children = []
        self._data = ''
        
    def __call__(self, data):
        self._data = data
        
    def __getitem__(self, item):
        return self._children[item]    
     
    def add(self, child):
        name = self._name
        parent = child._parent

        if parent == name:
            self._children.append(child)
        else:
            raise ContextError('Child object matches parent object')
    
    @classmethod
    def add_edge(cls, parent_string, node_object):
        cls._add(parent_string, node_object)
        
    @classmethod
    def display(cls, style='class'):
        styles = ['class', 'data', 'html']
        assert style in styles
        if Node.head:
            Node[Node.head]._display(style)
            
    def _display(self, style, depth=0):
        def show(msg):
            print msg
            
        {'class': lambda : show('    ' * depth + repr(self)),
        'data': lambda : show('    ' * depth + str(self._data)),
        'html': lambda : display(HTML(self._data))
        }[style]()
        
        for child in self._children:
            child._display(style, depth+1)
                    

class PresNode(Node):    
    def __init__(self):
        Node.__init__(self)

class SlideNode(PresNode):
    def __init__(self):
        Node.__init__(self)
        Node.add_edge(self._parent, self)

class SubSlideNode(SlideNode):
    def __init__(self):
        Node.__init__(self)
        Node.add_edge(self._parent, self)


class Slide(object):
    def __init__(self, layout=1, buf=None):
        self._layout = layout
        self._buf = self._make_buffer(buf)
        self._node = Node()
        if self._isPres():
            self._node = Node()
        self._tmp_buffer = None
        self._fig = None

    def __enter__(self):
        self._tmp_buffer = sys.stdout
        sys.stdout = self._buf
        return self
    
    
    def __exit__(self, type, value, traceback):
        sys.stdout = self._tmp_buffer
        self._tmp_buffer = None
        html = self._make_html()
        self._node(html)
        plt.close()
        self._buf.close()
        self._node.pop()
    

    def display(self):
        self._node._display('html')


    def _isPres(self):
        isPres = isinstance(self._node, PresNode)
        isSlide = isinstance(self._node, SlideNode)
        return isPres and not isSlide

    def _make_html(self):
        image = self._get_image()
        text = self._buf.getvalue()
        html = HTMLWriter(image, text, self._layout)
        return html

    
    @staticmethod
    def _get_image():
        fig = plt.gcf()
        if fig.axes:
            image = mpld3.fig_to_html(fig)
            fig.axes
        else:
            image = ''
        return image
    
    @staticmethod
    def _make_buffer(buf):
        if isinstance(buf, str):
            buf = open(buf, 'wb')
        elif buf is None:
            buf = HTMLBuffer()
        else:
            buf = buf
        return buf

