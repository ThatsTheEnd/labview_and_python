"""NiceGUI dashboard for the demo."""

from __future__ import annotations

import asyncio
import logging
from typing import Any, Dict

import plotly.graph_objects as go
from nicegui import app, ui

from shared.contracts import AnalysisResult, RawMeasurement

from .service import UIService

logger = logging.getLogger(__name__)


class DemoDashboard:
    def __init__(self, service: UIService) -> None:
        self.service = service
        self.current_correlation_id: str | None = None
        self.raw_data: RawMeasurement | None = None
        self.analysis_result: AnalysisResult | None = None
        self.raw_plot_element = None
        self.result_plot_element = None
        
        service.set_raw_handler(self._handle_raw)
        service.set_result_handler(self._handle_result)
        service.set_heartbeat_handler(self._handle_heartbeat)

    def _handle_raw(self, routing_key: str, payload: Dict[str, Any]) -> None:
        self.raw_data = RawMeasurement.from_dict(payload)
        logger.info("Received raw data: %d samples", len(self.raw_data.values))
        self._update_raw_plot()

    def _handle_result(self, routing_key: str, payload: Dict[str, Any]) -> None:
        self.analysis_result = AnalysisResult.from_dict(payload)
        logger.info("Received analysis result: health=%.2f", self.analysis_result.health_score)
        self._update_result_display()

    def _handle_heartbeat(self, routing_key: str, payload: Dict[str, Any]) -> None:
        logger.debug("Received heartbeat: %s", payload)

    def _update_raw_plot(self) -> None:
        if self.raw_data and self.raw_plot_element is not None:
            if len(self.raw_data.timestamps) > 0:
                # Update correlation ID and stats labels
                self.raw_id_label.set_text(f"Correlation ID: {self.raw_data.correlation_id[:8]}...")
                self.raw_info_label.set_text(f"Samples: {len(self.raw_data.values)} | Rate: {self.raw_data.sampling_rate_hz} Hz")
                self.raw_stats_label.set_text(f"Min: {min(self.raw_data.values):.3f} | Max: {max(self.raw_data.values):.3f}")
                
                # Create Plotly figure
                fig = go.Figure()
                fig.add_trace(go.Scatter(
                    x=self.raw_data.timestamps,
                    y=self.raw_data.values,
                    mode='lines',
                    name='Signal',
                    line=dict(color='#1f77b4', width=1.5)
                ))
                fig.update_layout(
                    title=None,
                    xaxis_title="Time (s)",
                    yaxis_title="Signal Value",
                    hovermode='x unified',
                    margin=dict(l=40, r=20, t=20, b=40),
                    height=300
                )
                fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='lightgray')
                fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='lightgray')
                
                self.raw_plot_element.update_figure(fig)

    def _update_result_display(self) -> None:
        if self.analysis_result and self.result_plot_element is not None:
            # Update correlation ID and peaks labels
            self.result_id_label.set_text(f"Correlation ID: {self.analysis_result.correlation_id[:8]}...")
            
            peaks_text = "Peak Frequencies (Hz): " + ", ".join(
                f"{freq:.1f}" for freq in self.analysis_result.peak_frequencies_hz[:5]
            )
            self.result_peaks_label.set_text(peaks_text)
            
            # Create Plotly gauge figure
            fig = go.Figure()
            
            fig.add_trace(go.Indicator(
                mode="gauge+number+delta",
                value=self.analysis_result.health_score * 100,
                domain={'x': [0, 1], 'y': [0, 1]},
                gauge={
                    'axis': {'range': [0, 100]},
                    'bar': {'color': '#1f77b4'},
                    'steps': [
                        {'range': [0, 50], 'color': '#ff6b6b'},
                        {'range': [50, 80], 'color': '#ffd93d'},
                        {'range': [80, 100], 'color': '#6bcf7f'},
                    ],
                    'threshold': {
                        'line': {'color': 'red', 'width': 4},
                        'thickness': 0.75,
                        'value': 80
                    }
                },
                number={'suffix': '%'},
                title={'text': 'Health Score'}
            ))
            
            fig.update_layout(
                margin=dict(l=20, r=20, t=60, b=20),
                height=300,
                font={'size': 14}
            )
            
            self.result_plot_element.update_figure(fig)

    async def _on_start_clicked(self) -> None:
        sampling_rate = float(self.sampling_rate_input.value)
        duration = float(self.duration_input.value)
        fault_enabled = self.fault_toggle.value
        
        self.current_correlation_id = await self.service.send_start(
            sampling_rate_hz=sampling_rate,
            duration_s=duration,
            fault_enabled=fault_enabled,
        )
        
        self.correlation_label.set_text(f"Correlation ID: {self.current_correlation_id}")
        ui.notify(f"Started measurement: {self.current_correlation_id[:8]}...", type="positive")

    async def _on_stop_clicked(self) -> None:
        if self.current_correlation_id:
            await self.service.send_stop(self.current_correlation_id)
            ui.notify("Stop command sent", type="info")

    async def _on_shutdown_clicked(self) -> None:
        await self.service.send_shutdown_all()
        ui.notify("Shutdown command sent to all modules", type="warning")
        await asyncio.sleep(0.5)  # Give time for RabbitMQ message to send
        app.shutdown()

    def build(self) -> None:
        with ui.header().classes('bg-blue-600 text-white'):
            ui.label("RabbitMQ Demo: LabVIEW & Python Integration").classes('text-h4')

        with ui.column().classes('w-full p-4'):
            # Control Panel
            with ui.card().classes('w-full'):
                ui.label("Control Panel").classes('text-h5')
                
                with ui.row():
                    self.sampling_rate_input = ui.number(
                        label="Sampling Rate (Hz)",
                        value=1000.0,
                        min=100.0,
                        max=10000.0,
                    ).classes('w-40')
                    
                    self.duration_input = ui.number(
                        label="Duration (s)",
                        value=1.0,
                        min=0.1,
                        max=10.0,
                    ).classes('w-40')
                    
                    self.fault_toggle = ui.checkbox("Enable Fault", value=False)

                with ui.row():
                    ui.button("Start Measurement", on_click=self._on_start_clicked).props('color=positive')
                    ui.button("Stop", on_click=self._on_stop_clicked).props('color=warning')
                    ui.button("Shutdown All", on_click=self._on_shutdown_clicked).props('color=negative')

                self.correlation_label = ui.label("Correlation ID: None").classes('text-sm text-gray-600')

            # Data Display
            with ui.row().classes('w-full gap-4'):
                # Raw Data
                with ui.card().classes('flex-1'):
                    ui.label("Raw Measurement Data").classes('text-h6')
                    
                    # Header labels
                    self.raw_id_label = ui.label("Correlation ID: None").classes('text-xs text-gray-500')
                    self.raw_info_label = ui.label("Samples: 0 | Rate: 0 Hz")
                    self.raw_stats_label = ui.label("Min: 0.000 | Max: 0.000")
                    
                    # Create placeholder Plotly figure
                    empty_fig = go.Figure()
                    empty_fig.update_layout(
                        title="Waiting for data...",
                        xaxis_title="Time (s)",
                        yaxis_title="Signal Value",
                        height=300,
                        margin=dict(l=40, r=20, t=40, b=40)
                    )
                    self.raw_plot_element = ui.plotly(empty_fig).classes('w-full')

                # Analysis Results
                with ui.card().classes('flex-1'):
                    ui.label("Analysis Results").classes('text-h6')
                    
                    self.result_id_label = ui.label("Correlation ID: None").classes('text-xs text-gray-500')
                    self.result_peaks_label = ui.label("Peak Frequencies (Hz): —")
                    
                    # Create placeholder gauge figure
                    empty_gauge = go.Figure()
                    empty_gauge.add_trace(go.Indicator(
                        mode="gauge+number",
                        value=0,
                        domain={'x': [0, 1], 'y': [0, 1]},
                        gauge={'axis': {'range': [0, 100]}},
                        title={'text': 'Health Score'}
                    ))
                    empty_gauge.update_layout(
                        height=300,
                        margin=dict(l=20, r=20, t=60, b=20)
                    )
                    self.result_plot_element = ui.plotly(empty_gauge).classes('w-full')
