import flet as ft 
from views.search_results import SearchResult
from youtube import Youtube

@ft.control
class Dashboard(ft.View):
    def __init__(self, user, navigation_bar):
        super().__init__(navigation_bar = navigation_bar)
        self.user = user 

    def init(self):
        self.route = "/"
        self.horizontal_alignment = ft.CrossAxisAlignment.CENTER

        self.search_results_ref = ft.Ref[ft.Column]()
        self.search_bar_ref = ft.Ref[ft.TextField]()
        self.controls = [
            self.createLayout()
        ]
    
    def createPlaceholder(self):
        return ft.Column( 
            expand = True,
            ref = self.search_results_ref,
            horizontal_alignment = ft.CrossAxisAlignment.CENTER,          
            controls = [
                ft.Image(expand = True, fit = ft.BoxFit.CONTAIN, src = "notes_dashboard.gif", width = 250, height = 250),
                ft.Text("LOWERTUNE", size = 24),
            ]
        )

    def createLayout(self):
        return ft.SafeArea(
            content = ft.Column(
                horizontal_alignment = ft.CrossAxisAlignment.CENTER,
                spacing = 10,
                controls = [
                    ft.TextField(ref = self.search_bar_ref, expand = True, label = "Search", on_submit = self.submitSearch),
                    self.createPlaceholder()
                ]  
            )
        )

    def createLoadingCircle(self):
        self.search_results_ref.current.controls.clear()

        self.search_results_ref.current.height = None
        self.search_results_ref.current.scroll = None

        self.search_results_ref.current.controls.append(
            ft.Container(
                alignment = ft.Alignment.CENTER,
                content = ft.ProgressRing(width = 150, height = 150)
            )
        )
        self.page.update()

    def createNoResult(self):
        self.search_results_ref.current.controls.clear()
        self.search_results_ref.current.controls.append(
            ft.Column(
                horizontal_alignment = ft.CrossAxisAlignment.CENTER,
                controls = [
                    ft.Image(expand = True, fit = ft.BoxFit.CONTAIN, src = "no_results.gif", width = 250, height = 250),
                    ft.Text("No Results Found!", size = 24),    
                ]
            )
        )
        self.page.update()

    def createResults(self, results):
        self.search_results_ref.current.controls.clear()

        self.search_results_ref.current.height = self.page.height - 100 # height - navigation bar
        self.search_results_ref.current.scroll = ft.ScrollMode.ALWAYS

        for result in results:
            self.search_results_ref.current.controls.append(
                SearchResult(result["title"], result["uploader"], result["duration_string"], result["thumbnail"], result["webpage_url"], self.handleResultClick)
            )
        self.page.update() 

    def hideSearchBar(self):
        self.search_bar_ref.current.visible = False
        self.vertical_alignment = ft.MainAxisAlignment.CENTER
        self.page.update()
    
    def showSearchBar(self):
        self.search_bar_ref.current.visible = True
        self.vertical_alignment = None
        self.page.update()

    def handleSearch(self, music_name):
        self.createLoadingCircle()
        self.hideSearchBar()
        results = Youtube.search(music_name)

        if results is None:
            self.createNoResult()
        else:
            self.createResults(results)
        self.showSearchBar()

    
    def submitSearch(self, e):
        music_name = e.control.value
        if music_name:
            self.page.run_thread(self.handleSearch, music_name)
    
    async def handleResultClick(self, e):
        await self.page.player_launch(e.control.video_url)
     