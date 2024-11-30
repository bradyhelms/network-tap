#include <iostream>
#include "IPv4Layer.h"
#include "EthLayer.h"
#include "Packet.h"
#include "PcapFileDevice.h"
#include "PcapLiveDeviceList.h"
#include "SystemUtils.h"
#include "MacAddress.h"

class PacketInterceptor {
private:
    pcpp::PcapLiveDevice* inDevice;
    pcpp::PcapLiveDevice* outDevice;
    pcpp::MacAddress      newMacAddress;
    
public:
    PacketInterceptor(const std::string& inInterface, const std::string& outInterface, const std::string& newMac) {
        // Get the input and output network interfaces
        inDevice = pcpp::PcapLiveDeviceList::getInstance().getPcapLiveDeviceByName(inInterface);
        outDevice = pcpp::PcapLiveDeviceList::getInstance().getPcapLiveDeviceByName(outInterface);
        
        if (!inDevice || !outDevice) {
            throw std::runtime_error("Could not find one or both network interfaces");
        }
        
        newMacAddress = pcpp::MacAddress(newMac);
    }
    
    bool init() {
        if (!inDevice->open()) {
            return false;
        }
        
        if (!outDevice->open()) {
            inDevice->close();
            return false;
        }
        
        return true;
    }
    
    static void onPacketArrives(pcpp::RawPacket* rawPacket, pcpp::PcapLiveDevice* dev, void* cookie) {
        auto* interceptor = static_cast<PacketInterceptor*>(cookie);
        
        // Parse and create a new modifiable packet
        pcpp::Packet parsedPacket(rawPacket);
        pcpp::Packet modifiedPacket = parsedPacket;
        
        // Get Ethernet layer
        pcpp::EthLayer* ethLayer = modifiedPacket.getLayerOfType<pcpp::EthLayer>();
        if (ethLayer != nullptr) {
            std::cout << "\n=== Ethernet Header ===" << std::endl;
            std::cout << "Source MAC:\t"             << ethLayer->getSourceMac() << std::endl;
            std::cout << "Dest MAC:\t"               << ethLayer->getDestMac() << std::endl;
            
            // Modify source MAC address
            ethLayer->setSourceMac(interceptor->newMacAddress);
            std::cout << "New src MAC:\t"            << ethLayer->getSourceMac() << std::endl;
        }
        
        // Get IPv4 layer
        pcpp::IPv4Layer* ipLayer = modifiedPacket.getLayerOfType<pcpp::IPv4Layer>();
        if (ipLayer != nullptr) {
            std::cout << "\n=== IPv4 Header ==="     << std::endl;
            std::cout << "Source IP:\t"              << ipLayer->getSrcIPAddress() << std::endl;
            std::cout << "Dest IP:\t"                << ipLayer->getDstIPAddress() << std::endl;
            std::cout << "TTL:\t"                    << (int)ipLayer->getIPv4Header()->timeToLive << std::endl;
        }
        
        // Compute new packet
        modifiedPacket.computeCalculateFields();
        
        // Convert modified packet back to raw packet and send
        pcpp::RawPacket* newRawPacket = modifiedPacket.getRawPacket();
        interceptor->outDevice->sendPacket(*newRawPacket);
    }
    
    void start() {
        inDevice->startCapture(onPacketArrives, this);
    }
    
    void stop() {
        inDevice->stopCapture();
        inDevice->close();
        outDevice->close();
    }
};

int main(int argc, char* argv[]) {
    if (argc != 4) {
        std::cerr << "Usage: " << argv[0] 
                 << " <input_interface> <output_interface> <new_mac_address>" << std::endl;
        std::cerr << "Example: " << argv[0] 
                 << " eth0 eth1 aa:bb:cc:dd:ee:ff" << std::endl;
        return 1;
    }
    
    try {
        PacketInterceptor interceptor(argv[1], argv[2], argv[3]);
        
        if (!interceptor.init()) {
            std::cerr << "Failed to initialize packet interceptor" << std::endl;
            return 1;
        }
        
        std::cout << "Starting packet interception..." << std::endl;
        interceptor.start();
        
        std::cout << "Press enter to stop..." << std::endl;
        std::cin.get();
        
        interceptor.stop();
        
    } catch (const std::exception& e) {
        std::cerr << "Error: " << e.what() << std::endl;
        return 1;
    }
    
    return 0;
}
