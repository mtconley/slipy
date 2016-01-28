from StringIO import StringIO

def HTMLWriter(image, sentence, layout=1):
    """HTML formatter for two panel slide

    Parameters
    ---------
    image : unicode
        d3 object to display

    sentence : str
        Plot description and commentary

    Notes
    -----
    Current function is placeholder for more robust factory using same API
    """
    if len(image) + len(sentence) == 0:
        return ''

    sentence = sentence.replace(' ', '&nbsp;')
    sentence = sentence.replace('\n', '<br>')

    html = """
        <div class="slide_container" style="width:840px;display:inline-block;">
            <div class="figure_box" style="display:inline-block; float:left;">
                {image}
            </div>

            <div class="description_box" style="font-size:18px;padding-top:60px;font-family:Century Gothic;">
                {sentence}
            </div>
        </div>
    """.format(image=image, sentence=sentence)
    
    return html


class HTMLBuffer(StringIO):
    """Buffer adapter to parse python data to HTML"""
    def write(self, msg):
        try:
            msg = eval(msg)
                        
            if isinstance(msg, list):
                msg = self._list_to_ol(msg)
            elif isinstance(msg, set):
                msg = self._list_to_ul(msg)
            else:
                raise TypeError('{} not recognized as list or set'.format(msg))
            
        except Exception as e:
            msg = msg.replace(' ', '&nbsp;')
            msg = msg.replace('\n', '<br>')
            msg = msg.replace('\t', '&nbsp;' * 4)

        StringIO.write(self, msg)
        
    def _list_to_list(self, msg, list_type):
        msg = """
              <{0}>
                  <li>{1}
                  </li>
              </{0}>
              """.format(
                list_type, '</li>\n<li>'.join(map(str, msg))
              )
        return msg
    
    def _list_to_ol(self, msg):
        msg = self._list_to_list(msg, 'ol')
        return msg
    
    def _list_to_ul(self, msg):
        msg = self._list_to_list(msg, 'ul')
        return msg