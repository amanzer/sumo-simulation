import xml.etree.ElementTree as ET
import matplotlib.pyplot as plt


tree = ET.parse('fcd.xml')
root = tree.getroot()


timedata = []

counter = 0

for i, timestep in enumerate(root.iter('timestep')):
    # Count the number of vehicle elements in the current timestep
    num_vehicles = len(timestep.findall('vehicle'))
    # Store the count in timedata at the correct index
    timedata.append(num_vehicles)


plt.figure()


x_values = list(range(len(timedata)))

plt.plot(x_values, timedata)

# Label the axes
plt.xlabel('Timestep')
plt.ylabel('Number of vehicles')


plt.title('Number of vehicles over timesteps')
plt.savefig("nb_vehicules.png")
plt.show()
