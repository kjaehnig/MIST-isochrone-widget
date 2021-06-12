





class MIST_isochrone_class():
    """Base class for generating isochrones using 
    ISOCHRONES package
    """
    def __init__(self):
        self.num_stars = 1000
        self.IMF = None
        self.masses = None
        self.tracks = None
        self.has_masses = False
        self.has_tracks = False

        self.iso_bounds = {
            'age': [5.1, 12.5],
            'av' : [0.0, 6.0],
            'dist' : [1.0, 30000],
            'feh' : [-4, 0.49] ## going out of feh lims will crash python
        }

    def generate_mass(self, N=None, IMF='chabrier'):
        """
        Generate an initial IMF distribution of masses
        """
        if N is None :
            N=self.num_stars
        if IMF is 'chabrier':
            from isochrones.priors import ChabrierPrior as iso_IMF
            self.IMF='chabrier'
        elif IMF is 'salpeter':
            from isochrones.priors import SalpeterPrior as iso_IMF
            self.IMF='salpetr'
        masses = iso_IMF().sample(N)
        self.masses = masses
        self.has_masses = True


    def get_tracks(self, TRACKS=False, BASIC=False):
        from isochrones import get_ichrone
        """
        Get evolutionary tracks to generate isochrones
        """
        tracks = get_ichrone('mist', tracks=TRACKS, basic=BASIC)
        self.has_tracks = True
        self.tracks = tracks


    def generate_photometry(self, 
                            age=7.0, 
                            av=1.0, 
                            dist=10.0, 
                            feh=0.00):
        """
        Generate synthetic photometry for isochrone
        """
        if self.has_masses is False:
            self.generate_mass()
        if self.has_tracks is False:
            self.get_tracks()

        if feh < -4 or feh > 0.49:
            raise Exception("GOING OUTSIDE OF FeH LIMITS WILL CRASH PYTHON")
            return
        iso_df = self.tracks.generate(self.masses,
                                    age,
                                    feh,
                                    distance=dist,
                                    AV=av)
        iso_df['BP_RP'] = iso_df.BP_mag.values - iso_df.RP_mag.values
        iso_df = iso_df.dropna()

        return iso_df
