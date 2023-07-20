import os
import sys

class Simulation:
    """
    Class for simulating traffic in a given osm file with random TAZs and trips
    """

    def __init__(self, osm_file : str, beginning =0, interval_end =3600, probability=0.5, router="duarouter") -> None:

        self.osm_file_name = osm_file
        self.beginning_value = beginning
        self.end_value = interval_end
        self.probability_value = probability


        self.osm_file_path = os.path.join(os.getcwd(), self.osm_file_name)
        self.net_file_path = self.osm_file_path + '.net.xml'
        self.taz_file_path = self.osm_file_path + '.taz.xml'
        self.poly_file_path = self.osm_file_path + '.poly.xml'
        self.trips_file_path = self.osm_file_path + '.trips.xml'
        self.routes_file_path = self.osm_file_path + '.routes.xml'

        self.generate_network()
        self.generate_taz_poly()
        self.generate_trips()
        self.generate_routes(router)
        self.generate_config()

    def generate_network(self) -> None:
        """
        Generate the network file from the osm file
        """
        os.system(f"netconvert --osm-files {self.osm_file_path} --output-file {self.net_file_path}")
    
    def generate_taz_poly(self) -> None:
        """
        Generate the poly file from the network and osm files
        """
        os.system(f"python $SUMO_HOME/tools/generateBidiDistricts.py {self.net_file_path} -o {self.taz_file_path} ")

        os.system(f"polyconvert --net-file {self.net_file_path} --osm-files {self.osm_file_path} --type-file $SUMO_HOME/data/typemap/osmPolyconvert.typ.xml -o {self.poly_file_path}")

    def generate_trips(self) -> None:
        """
        Generate the trips file from the network and poly files
        b : beginning time
        e : end time
        p : probability of a vehicle spawning at a given interval
        t : poly file
        """
        os.system(f"python $SUMO_HOME/tools/randomTrips.py -n {self.net_file_path} -b {self.beginning_value} \
                   -e {self.end_value} -p {self.probability_value} -t {self.taz_file_path} -o {self.trips_file_path} ")

    def generate_routes(self, router:str) -> None:
        """
        Generate the routes file from the trips file
        """
        if router == "duarouter":
            os.system(f"duarouter --net-file {self.net_file_path} --route-files {self.trips_file_path} -o {self.routes_file_path} ")
    

    def generate_config(self) -> None:
        configuration_file = f"""<configuration>
            <input>
                <net-file value="{self.net_file_path}"/>
                <route-files value="{self.routes_file_path}"/>
                <additional-files value="{self.poly_file_path}"/>
            </input>


        </configuration>"""

        with open(f"{self.osm_file_name}.sumocfg", "w") as f:
            f.write(configuration_file)
    

    def run_simulation(self, tripinfo=True, edgedata=False, rerouter=False) -> None:
        """
        Run the simulation using command line with the configuration file
        """
        command=f"sumo -c {self.osm_file_name}.sumocfg"

        if tripinfo:
            command += " --tripinfo-output tripinfo.xml"
        if edgedata:
            command += " --edgedata-output edgeData.xml"
        if rerouter:
            command += " -a rerouter.add.xml --ignore-route-errors"

        os.system(command)


    def clean_files(self) -> None:
        """
        Clean the generated files
        """
        os.remove(self.net_file_path)
        os.remove(self.poly_file_path)
        os.remove(self.trips_file_path)
        os.remove(self.routes_file_path)
        os.remove(self.routes_file_path[:-4] + ".alt.xml")
        os.remove(f"{self.osm_file_name}.sumocfg")



if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: provide an osm file name as argument")
        sys.exit(1)


    sim = Simulation(sys.argv[1])
    sim.run_simulation()


    #sim.clean_files() 
