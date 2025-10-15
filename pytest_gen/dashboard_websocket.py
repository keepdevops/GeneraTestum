"""
Dashboard WebSocket management and handlers.
"""

import json
import asyncio
from datetime import datetime
from typing import Dict, List, Any
from fastapi import WebSocket, WebSocketDisconnect
from .dashboard_models import DashboardEvent


class DashboardWebSocketManager:
    """Manages WebSocket connections and real-time updates."""
    
    def __init__(self, data_collector):
        self.data_collector = data_collector
        self.connected_clients: List[WebSocket] = []
        self.update_interval = 30  # seconds
    
    async def connect(self, websocket: WebSocket):
        """Accept WebSocket connection."""
        await websocket.accept()
        self.connected_clients.append(websocket)
        
        # Send initial data
        await self._send_dashboard_data(websocket)
    
    async def disconnect(self, websocket: WebSocket):
        """Handle WebSocket disconnection."""
        if websocket in self.connected_clients:
            self.connected_clients.remove(websocket)
    
    async def handle_websocket(self, websocket: WebSocket):
        """Handle WebSocket connection lifecycle."""
        await self.connect(websocket)
        
        try:
            while True:
                # Wait for client messages
                data = await websocket.receive_text()
                await self._handle_client_message(websocket, data)
                
        except WebSocketDisconnect:
            await self.disconnect(websocket)
        except Exception as e:
            print(f"WebSocket error: {e}")
            await self.disconnect(websocket)
    
    async def _handle_client_message(self, websocket: WebSocket, message: str):
        """Handle messages from WebSocket clients."""
        try:
            data = json.loads(message)
            message_type = data.get("type")
            
            if message_type == "ping":
                await websocket.send_text(json.dumps({"type": "pong", "timestamp": datetime.now().isoformat()}))
            
            elif message_type == "request_update":
                await self._send_dashboard_data(websocket)
            
            elif message_type == "subscribe":
                event_type = data.get("event_type")
                await self._subscribe_to_events(websocket, event_type)
            
            elif message_type == "unsubscribe":
                event_type = data.get("event_type")
                await self._unsubscribe_from_events(websocket, event_type)
                
        except json.JSONDecodeError:
            await websocket.send_text(json.dumps({"error": "Invalid JSON"}))
        except Exception as e:
            await websocket.send_text(json.dumps({"error": str(e)}))
    
    async def _send_dashboard_data(self, websocket: WebSocket):
        """Send complete dashboard data to client."""
        try:
            data = self.data_collector.collect_all_data()
            event = DashboardEvent(
                type="dashboard_update",
                data=self._serialize_data(data),
                timestamp=datetime.now()
            )
            
            await websocket.send_text(json.dumps({
                "type": event.type,
                "data": event.data,
                "timestamp": event.timestamp.isoformat()
            }))
            
        except Exception as e:
            await websocket.send_text(json.dumps({
                "type": "error",
                "message": f"Failed to send data: {str(e)}",
                "timestamp": datetime.now().isoformat()
            }))
    
    async def _subscribe_to_events(self, websocket: WebSocket, event_type: str):
        """Subscribe client to specific event types."""
        # Implementation would depend on specific event types
        await websocket.send_text(json.dumps({
            "type": "subscribed",
            "event_type": event_type,
            "timestamp": datetime.now().isoformat()
        }))
    
    async def _unsubscribe_from_events(self, websocket: WebSocket, event_type: str):
        """Unsubscribe client from specific event types."""
        await websocket.send_text(json.dumps({
            "type": "unsubscribed",
            "event_type": event_type,
            "timestamp": datetime.now().isoformat()
        }))
    
    async def broadcast_update(self, event: DashboardEvent):
        """Broadcast update to all connected clients."""
        if not self.connected_clients:
            return
        
        message = json.dumps({
            "type": event.type,
            "data": event.data,
            "timestamp": event.timestamp.isoformat()
        })
        
        # Send to all connected clients
        disconnected_clients = []
        for client in self.connected_clients:
            try:
                await client.send_text(message)
            except Exception:
                disconnected_clients.append(client)
        
        # Remove disconnected clients
        for client in disconnected_clients:
            await self.disconnect(client)
    
    async def start_periodic_updates(self):
        """Start periodic data updates for all clients."""
        while True:
            try:
                await asyncio.sleep(self.update_interval)
                
                if self.connected_clients:
                    data = self.data_collector.collect_all_data()
                    event = DashboardEvent(
                        type="periodic_update",
                        data=self._serialize_data(data),
                        timestamp=datetime.now()
                    )
                    
                    await self.broadcast_update(event)
                    
            except Exception as e:
                print(f"Periodic update error: {e}")
    
    def _serialize_data(self, data) -> Dict[str, Any]:
        """Serialize dashboard data for WebSocket transmission."""
        return {
            "system_status": data.system_status.value,
            "last_updated": data.last_updated.isoformat(),
            "metrics": [
                {
                    "name": metric.name,
                    "value": metric.value,
                    "unit": metric.unit,
                    "category": metric.category.value
                }
                for metric in data.metrics
            ],
            "active_jobs": [
                {
                    "id": job.id,
                    "name": job.name,
                    "status": job.status.value,
                    "progress": job.progress
                }
                for job in data.active_jobs
            ],
            "alerts": [
                {
                    "id": alert.id,
                    "message": alert.message,
                    "level": alert.level.value,
                    "category": alert.category.value,
                    "resolved": alert.resolved
                }
                for alert in data.alerts
            ]
        }
