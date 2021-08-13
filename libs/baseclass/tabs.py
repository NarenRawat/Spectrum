from kivymd.uix.relativelayout import MDRelativeLayout
from kivymd.uix.tab import MDTabsBase


class SongsTab(MDRelativeLayout, MDTabsBase):
    def __init__(self, **kwargs):
        super(SongsTab, self).__init__(**kwargs)


class AlbumsTab(MDRelativeLayout, MDTabsBase):
    def __init__(self, **kwargs):
        super(AlbumsTab, self).__init__(**kwargs)


class ArtistsTab(MDRelativeLayout, MDTabsBase):
    def __init__(self, **kwargs):
        super(ArtistsTab, self).__init__(**kwargs)
