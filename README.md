# Egress Peer Engineering
Egree Peer Engineering with Healthbot and Northstar

Egress Peer Engineering enables the operator to direct traffic to a specific peer, set of peers, or a specific link to a peer based on business policy (cost) and performance information (latency, traffic loss, etc) other than the best path. The need for engineering the way that traffic exits the service provider AS is critical for ensuring cost efficiency while providing a good end user experience at the same time. 


In this demo:  
1.Healthbot monitors packet loss on peering links;

2.When a peering link is suffering from packet loss,  Healthbot uses User Defined Function to trigger API call to Northstar to steer the traffic by mapping the demands to a pre-configured colored SRTE LSP
