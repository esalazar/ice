# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

# this module is responsible for rewriting chrome javascript source files.
# Modifcations it makes are:
# * All chrome identifiers are replaced with wrapped_chrome
# * disallow eval
# * disallow access to __proto__ and function constructor
# * rewrites all array accesses to arrayAccess(array, subscript)

try:
    import re
    import sys
    from slimit import ast, parser
    import lxml.html
    import lxml.html.clean
    import wrappers
except ImportError:
    print """slimit or lxml is not installed. Please run

    $ sudo easy_install slimit
    $ sudo easy_install lxml
    """
    sys.exit(1)

permsToModulesMap = {}
permsToModulesMap["bookmarks"] = "bookmarks"
permsToModulesMap["cookies"] = "cookies"
permsToModulesMap["history"] = "history"
permsToModulesMap["management"] = "management"
permsToModulesMap["geolocation"] = "geolocation"


processedFiles = []

def rewriteJs(sourceFiles, perms):
    for js in sourceFiles:
        name = js.rsplit("/", 1)[1] # get filename
        # don't process this file if we've seen it already
        if name in processedFiles:
            continue
        # refuse to rewrite extensions with remote script inclusion
        if "http://" in js or "https://" in js:
            print """This extension tries to load a script from the internet
            and cannot be trusted. We refuse to rewrite it."""
            sys.exit(-1)
        with open(js, "r") as f:
            source = f.readlines()
        filteredSource = filter_js("\n".join(source))
        with open(js, "w") as f:
            # add iced coffee
            f.write(wrappers.iced_coffee)
            # write wrapped chrome.* APIs
            for perm, value in perms.iteritems():
                wrappedState = "passthrough" if value else "wrapped"
                f.write(wrappers.wrappers[permsToModulesMap[perm]][wrappedState])
            # write untouched passthrough wrappers
            for untouched in wrappers.untouched:
                f.write(wrappers.wrappers[untouched]["wrapped"])
            f.write(trustedLib)
            f.write("\n")
            f.write(filteredSource)
        processedFiles.append(name)

def rewriteHtml(sourceFiles, perms):
    for html in sourceFiles:
        with open(html, "r") as f:
            source = f.readlines()
            source = "\n".join(source)

        doc = lxml.html.fromstring(source)
        for el in doc.iter():
            if el.tag == 'script':
                if el.text is not None:
                    txt = ""
                    # add iced coffee
                    txt += wrappers.iced_coffee
                    # write wrapped chrome.* APIs
                    for perm, value in perms.iteritems():
                        wrappedState = "passthrough" if value else "wrapped"
                        txt += wrappers.wrappers[permsToModulesMap[perm]][wrappedState]
                    # write untouched passthrough wrappers
                    for untouched in wrappers.untouched:
                        txt += wrappers.wrappers[untouched]["wrapped"]
                    txt += trustedLib + "\n"
            
                    el.text = txt + filter_js(el.text)
                for a in el.attrib:
                    if a == "src":
                        rewriteJs([html.rsplit("/", 1)[0] + "/" + el.attrib[a]], perms)
        filteredSource = lxml.html.tostring(doc, method="html")

        with open(html, "w") as f:
            f.write(filteredSource)

def filter_js(s):
    jsParser = parser.Parser()
    tree = jsParser.parse(s)
    visitor = IceVisitor()
    return visitor.visit(tree)

trustedLib = """
// This function could be used in the future to check strings of
// array accesses.
// For now, it does nothing
function arrayAccess(array, subscript) {
    return array[bracket_check(subscript)];
}

// Prevents dangerous properties from being accessed
function bracket_check(input) {
    if (typeof(input) === "number") {
        return input;
    }

    var dangerous = ["__proto__", "prototype", "constructor", "__defineGetter__", "__defineSetter__"];
    var copied_input = "";
    var len = input.length;
    for (var j = 0; j < len; j++) {
        copied_input += input.charAt(j);
    }
    for (var i = 0; i < dangerous.length; i++) {
        if (dangerous[i] == copied_input) {
            throw Error("Illegal array subscript");
        }
    }
    return copied_input;
}
"""

class IceVisitor(object):

    def __init__(self):
        self.indent_level = 0

    def _make_indent(self):
        return ' ' * self.indent_level

    def visit(self, node):
        method = 'visit_%s' % node.__class__.__name__
        return getattr(self, method, self.generic_visit)(node)

    def generic_visit(self, node):
        return 'GEN: %r' % node

    def visit_Program(self, node):
        return '\n'.join(self.visit(child) for child in node)

    def visit_Block(self, node):
        s = '{\n'
        self.indent_level += 2
        s += '\n'.join(
                self._make_indent() + self.visit(child) for child in node)
        self.indent_level -= 2
        s += '\n' + self._make_indent() + '}'
        return s

    def visit_VarStatement(self, node):
        s = 'var %s;' % ', '.join(self.visit(child) for child in node)
        return s

    def visit_VarDecl(self, node):
        output = []
        output.append(self.visit(node.identifier))
        if node.initializer is not None:
            output.append(' = %s' % self.visit(node.initializer))
        return ''.join(output)

    def visit_Identifier(self, node):
        if node.value == "chrome":
            return "wrapped_chrome"
        return "%s" % node.value

    def visit_Assign(self, node):
        if node.op == ':':
            template = '%s%s %s'
        else:
            template = '%s %s %s'
        if getattr(node, '_parens', False):
            template = '(%s)' % template
        return template % (
                self.visit(node.left), node.op, self.visit(node.right))

    def visit_Number(self, node):
        return node.value

    def visit_Comma(self, node):
        return '%s, %s' % (self.visit(node.left), self.visit(node.right))

    def visit_EmptyStatement(self, node):
        return node.value

    def visit_If(self, node):
        s = 'if ('
        if node.predicate is not None:
            s += self.visit(node.predicate)
        s += ') '
        s += self.visit(node.consequent)
        if node.alternative is not None:
            s += ' else '
            s += self.visit(node.alternative)
        return s

    def visit_Boolean(self, node):
        return node.value

    def visit_For(self, node):
        s = 'for ('
        if node.init is not None:
            s += self.visit(node.init)
        if node.init is None:
            s += ' ; '
        elif isinstance(node.init, (ast.Assign, ast.Comma)):
            s += '; '
        else:
            s += ' '
        if node.cond is not None:
            s += self.visit(node.cond)
        s += '; '
        if node.count is not None:
            s += self.visit(node.count)
        s += ') ' + self.visit(node.statement)
        return s

    def visit_ForIn(self, node):
        if isinstance(node.item, ast.VarDecl):
            template = 'for (var %s in %s) '
        else:
            template = 'for (%s in %s) '
        s = template % (self.visit(node.item), self.visit(node.iterable))
        s += self.visit(node.statement)
        return s

    def visit_BinOp(self, node):
        if getattr(node, '_parens', False):
            template = '(%s %s %s)'
        else:
            template = '%s %s %s'
        return template % (
                self.visit(node.left), node.op, self.visit(node.right))

    def visit_UnaryOp(self, node):
        s = self.visit(node.value)
        if node.postfix:
            s += node.op
        elif node.op in ('delete', 'void', 'typeof'):
            s = '%s %s' % (node.op, s)
        else:
            s = '%s%s' % (node.op, s)
        if getattr(node, '_parens', False):
            s = '(%s)' % s
        return s

    def visit_ExprStatement(self, node):
        return '%s;' % self.visit(node.expr)

    def visit_DoWhile(self, node):
        s = 'do '
        s += self.visit(node.statement)
        s += ' while (%s);' % self.visit(node.predicate)
        return s

    def visit_While(self, node):
        s = 'while (%s) ' % self.visit(node.predicate)
        s += self.visit(node.statement)
        return s

    def visit_Null(self, node):
        return 'null'

    def visit_String(self, node):
        return node.value

    def visit_Continue(self, node):
        if node.identifier is not None:
            s = 'continue %s;' % self.visit_Identifier(node.identifier)
        else:
            s = 'continue;'
        return s

    def visit_Break(self, node):
        if node.identifier is not None:
            s = 'break %s;' % self.visit_Identifier(node.identifier)
        else:
            s = 'break;'
        return s

    def visit_Return(self, node):
        if node.expr is None:
            return 'return;'
        else:
            return 'return %s;' % self.visit(node.expr)

    def visit_With(self, node):
        s = 'with (%s) ' % self.visit(node.expr)
        s += self.visit(node.statement)
        return s

    def visit_Label(self, node):
        s = '%s: %s' % (
                self.visit(node.identifier), self.visit(node.statement))
        return s

    def visit_Switch(self, node):
        s = 'switch (%s) {\n' % self.visit(node.expr)
        self.indent_level += 2
        for case in node.cases:
            s += self._make_indent() + self.visit_Case(case)
        if node.default is not None:
            s += self.visit_Default(node.default)
        self.indent_level -= 2
        s += self._make_indent() + '}'
        return s

    def visit_Case(self, node):
        s = 'case %s:\n' % self.visit(node.expr)
        self.indent_level += 2
        elements = '\n'.join(self._make_indent() + self.visit(element)
                for element in node.elements)
        if elements:
            s += elements + '\n'
        self.indent_level -= 2
        return s

    def visit_Default(self, node):
        s = self._make_indent() + 'default:\n'
        self.indent_level += 2
        s += '\n'.join(self._make_indent() + self.visit(element)
                for element in node.elements)
        if node.elements is not None:
            s += '\n'
        self.indent_level -= 2
        return s

    def visit_Throw(self, node):
        s = 'throw %s;' % self.visit(node.expr)
        return s

    def visit_Debugger(self, node):
        return '%s;' % node.value

    def visit_Try(self, node):
        s = 'try '
        s += self.visit(node.statements)
        if node.catch is not None:
            s += ' ' + self.visit(node.catch)
        if node.fin is not None:
            s += ' ' + self.visit(node.fin)
        return s

    def visit_Catch(self, node):
        s = 'catch (%s) %s' % (
                self.visit(node.identifier), self.visit(node.elements))
        return s

    def visit_Finally(self, node):
        s = 'finally %s' % self.visit(node.elements)
        return s

    def visit_FuncDecl(self, node):
        self.indent_level += 2
        elements = '\n'.join(self._make_indent() + self.visit(element)
                for element in node.elements)
        self.indent_level -= 2

        s = 'function %s(%s) {\n%s' % (
                self.visit(node.identifier),
                ', '.join(self.visit(param) for param in node.parameters),
                elements,
                )
        s += '\n' + self._make_indent() + '}'
        return s

    def visit_FuncExpr(self, node):
        self.indent_level += 2
        elements = '\n'.join(self._make_indent() + self.visit(element)
                for element in node.elements)
        self.indent_level -= 2

        ident = node.identifier
        ident = '' if ident is None else ' %s' % self.visit(ident)

        header = 'function%s(%s)'
        if getattr(node, '_parens', False):
            header = '(' + header
        s = (header + ' {\n%s') % (
                ident,
                ', '.join(self.visit(param) for param in node.parameters),
                elements,
                )
        s += '\n' + self._make_indent() + '}'
        if getattr(node, '_parens', False):
            s += ')'
        return s

    def visit_Conditional(self, node):
        if getattr(node, '_parens', False):
            template = '(%s ? %s : %s)'
        else:
            template = '%s ? %s : %s'

        s = template % (
                self.visit(node.predicate),
                self.visit(node.consequent), self.visit(node.alternative))
        return s

    def visit_Regex(self, node):
        if getattr(node, '_parens', False):
            return '(%s)' % node.value
        else:
            return node.value

    def visit_NewExpr(self, node):
        s = 'new %s(%s)' % (
                self.visit(node.identifier),
                ', '.join(self.visit(arg) for arg in node.args)
                )
        return s

    def visit_DotAccessor(self, node):
        if getattr(node, '_parens', False):
            template = '(%s.%s)'
        else:
            template = '%s.%s'
        if id in ["__proto__", "prototype", "constructor", "__defineGetter__", "__defineSetter__"]:
            return ""

        s = template % (self.visit(node.node), self.visit(node.identifier))
        return s

    def visit_BracketAccessor(self, node):
        s = 'arrayAccess(%s, %s)' % (self.visit(node.node), self.visit(node.expr))
        return s

    def visit_FunctionCall(self, node):
        s = '%s(%s)' % (self.visit(node.identifier),
                ', '.join(self.visit(arg) for arg in node.args))
        return s

    def visit_Object(self, node):
        s = '{\n'
        self.indent_level += 2
        s += ',\n'.join(self._make_indent() + self.visit(prop)
                for prop in node.properties)
        self.indent_level -= 2
        if node.properties:
            s += '\n'
        s += self._make_indent() + '}'
        return s

    def visit_Array(self, node):
        s = '['
        length = len(node.items) - 1
        for index, item in enumerate(node.items):
            if isinstance(item, ast.Elision):
                s += ','
            elif index != length:
                s += self.visit(item) + ','
            else:
                s += self.visit(item)
        s += ']'
        return s

    def visit_This(self, node):
        return 'this'

