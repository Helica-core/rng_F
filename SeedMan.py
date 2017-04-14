#
#
#
#
#

class SeedMan:
    
    sf          = './seed/rngseed'
    rngFunc     = None
    seedsize    = 64
    reseed      = None

    def __init__(self, rngf, reseed):
        
        self.rngFunc = rngf
        self.reseed  = reseed

        try:
        
            s = self.ReadSeedFile()        
         
        except:
            
            self.WriteSeedFile()
        
        if s == -1 or len(s) != 64:
            
            self.WriteSeedFile()
        
        self.UpdateSeedFile()

    def ReadSeedFile(self):

        try:
            seed = open(self.sf, 'rb')
        
            s = seed.read(64)

            seed.close()

            return s
        except:
            
            return -1


    def WriteSeedFile(self):
        
        seed = open(self.sf , 'wb')
        
        seed.write(self.rngFunc(64))

        seed.close()

    
    def UpdateSeedFile(self ):
        
        s = self.ReadSeedFile() 

        assert len(s) == 64

        self.reseed(s)

        self.WriteSeedFile()



    
