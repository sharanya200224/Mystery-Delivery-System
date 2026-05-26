import json
import math
from typing import Dict, List, Tuple, Any
from collections import defaultdict

class FastBoxDeliverySystem:
    """Logistics simulator for FastBox delivery company"""
    
    def __init__(self, json_file_path: str):
        """Initialize the delivery system with data from JSON file"""
        self.json_file_path = json_file_path
        self.warehouses = {}
        self.agents = {}
        self.packages = []
        self.assignments = defaultdict(list)
        self.agent_stats = {}
        
    def load_data(self) -> None:
        """Load and parse JSON data manually"""
        with open(self.json_file_path, 'r') as file:
            data = json.load(file)
        
        # Parse warehouses
        for warehouse in data['warehouses']:
            self.warehouses[warehouse['id']] = tuple(warehouse['location'])
        
        # Parse agents
        for agent in data['agents']:
            self.agents[agent['id']] = tuple(agent['location'])
        
        # Parse packages
        for package in data['packages']:
            self.packages.append({
                'id': package['id'],
                'warehouse_id': package['warehouse_id'],
                'destination': tuple(package['destination'])
            })
    
    def calculate_distance(self, point1: Tuple[float, float], point2: Tuple[float, float]) -> float:
        """Calculate Euclidean distance between two points"""
        return math.sqrt((point2[0] - point1[0])**2 + (point2[1] - point1[1])**2)
    
    def find_nearest_agent(self, warehouse_location: Tuple[float, float]) -> str:
        """Find the nearest agent to a given warehouse"""
        min_distance = float('inf')
        nearest_agent = None
        
        for agent_id, agent_location in self.agents.items():
            distance = self.calculate_distance(warehouse_location, agent_location)
            if distance < min_distance:
                min_distance = distance
                nearest_agent = agent_id
        
        return nearest_agent
    
    def assign_packages_to_agents(self) -> None:
        """Assign each package to the nearest agent"""
        for package in self.packages:
            warehouse_location = self.warehouses[package['warehouse_id']]
            nearest_agent = self.find_nearest_agent(warehouse_location)
            self.assignments[nearest_agent].append(package)
    
    def calculate_delivery_distance(self, agent_start: Tuple[float, float], 
                                   warehouse: Tuple[float, float], 
                                   destination: Tuple[float, float]) -> float:
        """Calculate total distance for one delivery"""
        to_warehouse = self.calculate_distance(agent_start, warehouse)
        to_destination = self.calculate_distance(warehouse, destination)
        return to_warehouse + to_destination
    
    def simulate_deliveries(self) -> None:
        """Simulate the delivery process for all agents"""
        for agent_id, assigned_packages in self.assignments.items():
            total_distance = 0
            agent_current_location = self.agents[agent_id]
            
            print(f"\n--- Agent {agent_id} Simulation ---")
            
            for package in assigned_packages:
                warehouse_location = self.warehouses[package['warehouse_id']]
                destination = package['destination']
                
                delivery_distance = self.calculate_delivery_distance(
                    agent_current_location, warehouse_location, destination
                )
                
                total_distance += delivery_distance
                agent_current_location = destination
                
                print(f"  Delivered {package['id']}: Distance = {delivery_distance:.2f}")
            
            # Store statistics
            self.agent_stats[agent_id] = {
                'packages_delivered': len(assigned_packages),
                'total_distance': round(total_distance, 2)
            }
            
            print(f"  Total distance traveled: {total_distance:.2f}")
    
    def calculate_efficiency(self) -> Dict[str, Any]:
        """Calculate efficiency for each agent"""
        for agent_id, stats in self.agent_stats.items():
            if stats['packages_delivered'] > 0:
                efficiency = stats['total_distance'] / stats['packages_delivered']
                stats['efficiency'] = round(efficiency, 2)
            else:
                stats['efficiency'] = 0
        
        if self.agent_stats:
            best_agent = min(self.agent_stats.keys(), 
                           key=lambda x: self.agent_stats[x]['efficiency'])
        else:
            best_agent = None
        
        return {
            'agent_stats': self.agent_stats,
            'best_agent': best_agent
        }
    
    def generate_report(self) -> Dict[str, Any]:
        """Generate the final report"""
        efficiency_data = self.calculate_efficiency()
        
        report = {}
        for agent_id, stats in efficiency_data['agent_stats'].items():
            report[agent_id] = {
                'packages delivered': stats['packages_delivered'],
                'total distance': stats['total_distance'],
                'efficiency': stats['efficiency']
            }
        
        report['best_agent'] = efficiency_data['best_agent']
        return report
    
    def print_report(self, report: Dict[str, Any]) -> None:
        """Print the report"""
        print("\n📊 Generating report...")
        print("\n" + "="*50)
        print("DELIVERY REPORT")
        print("="*50)
        
        for agent_id, stats in report.items():
            if agent_id != 'best_agent':
                print(f"\nAgent {agent_id}:")
                print(f"  Packages delivered: {stats['packages delivered']}")
                print(f"  Total distance: {stats['total distance']}")
                print(f"  Efficiency: {stats['efficiency']}")
        
        print(f"\n{'='*50}")
        print(f"BEST AGENT: {report['best_agent']}")
        print(f"{'='*50}")
    
    def save_report_to_json(self, report: Dict[str, Any], output_file: str = 'report.json') -> None:
        """Save the delivery report to a JSON file"""
        with open(output_file, 'w') as file:
            json.dump(report, file, indent=2)
    
    def run_simulation(self) -> None:
        """Run the complete delivery simulation"""
        # Load data
        self.load_data()
        
        # Assign packages
        self.assign_packages_to_agents()
        
        # Simulate deliveries
        self.simulate_deliveries()
        
        # Generate and save report
        report = self.generate_report()
        self.print_report(report)
        self.save_report_to_json(report)


# Main execution
if __name__ == "__main__":
    delivery_system = FastBoxDeliverySystem('base_case.json')
    delivery_system.run_simulation()
