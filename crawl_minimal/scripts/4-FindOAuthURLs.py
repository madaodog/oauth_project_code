from crawl_minimal import PyChromeScript

class FindOAuthURLs(PyChromeScript):
    def __init__(self, browser, tab, url, settings, workdir, entry_config=None):
        super().__init__(browser, tab, url, settings, workdir)
        self.tab.Page.enable()
        self.tab.DOM.enable()
        self.tab.CSS.enable()
        self.tab.Target.setDiscoverTargets(discover=True)
        self.tab.Page.loadEventFired = self.wait_for_loaded
        self.max_visits_website = 5
        self.login_links = []
        self.confirm_links = []
        self.last_confirm_links = []
        self.site = self.url
        self.finished = False
        print("Starting script")

    def press_login_button(self):
        # Get the root node
        root = self.tab.DOM.getDocument()["root"]["nodeId"]
    
        # Select all buttons and links
        nodes = self.tab.DOM.querySelectorAll(nodeId=root, selector="button, a")
        
        # Iterate through the node IDs
        for node_id in nodes["nodeIds"]:
            print(f"Checking node {node_id}")
            attributes = self.tab.DOM.getAttributes(nodeId=node_id)["attributes"]
            print(f"Attributes: {attributes}")

            if "Continue with Google" in attributes:
                print("Found login button")
                self.login_links.append(node_id)
        
        self.click(self.login_links[0])
        
        
    def click(self, nodeId, **kwargs):
        # Initate click on element
        if nodeId == 0:
            return
        print("node being clicked on: " + str(nodeId))
        try:
            resolveNode = self.tab.DOM.resolveNode(nodeId=nodeId)
            RemoteObjectId = resolveNode.get('object').get("objectId")
            self.tab.Runtime.callFunctionOn(objectId=RemoteObjectId, functionDeclaration='(function() { this.click(); })')
        except:
            print("Invalid parameters")
        try:
            boxModel = self.tab.DOM.getBoxModel(nodeId=nodeId)["model"]
            boxModelContent = boxModel["content"]
            x = (boxModelContent[0] + boxModelContent[2]) / 2
            y = (boxModelContent[1] + boxModelContent[5]) / 2

            self.tab.Input.dispatchMouseEvent(type="mousePressed", x=x, y=y, button="left")
            print("Clicked!")
        except:
            print("Boxmodel failed on id", nodeId)
    

    def confirm_login(self):
        root = self.tab.DOM.getDocument()["root"]["nodeId"]
        nodes = self.tab.DOM.querySelectorAll(nodeId=root, selector="div")

        for node_id in nodes["nodeIds"]:
            attributes = self.tab.DOM.getAttributes(nodeId=node_id)["attributes"]
            print(f"Attributes: {attributes}")

            if "thesis742@gmail.com" in attributes:
                print("Found confirmation button")
                self.confirm_links.append(node_id)
                break
        
        self.click(self.confirm_links[0])
    
    def last_confirm_login(self):
        root = self.tab.DOM.getDocument()["root"]["nodeId"]
        nodes = self.tab.DOM.querySelectorAll(nodeId=root, selector="div")

        for node_id in nodes["nodeIds"]:
            attributes = self.tab.DOM.getAttributes(nodeId=node_id)["attributes"]
            print(f"Attributes: {attributes}")

            if "Doorgaan" in attributes:
                print("Found confirmation button")
                self.last_confirm_links.append(node_id)
                break
        self.click(self.last_confirm_links[0])

    
    def wait_for_loaded(self, **kwargs):
        #self.press_login_button()
        #self.confirm_login()
        self.last_confirm_login()
        self.finished = True
                

