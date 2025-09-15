/**
 * Data Monitor - Automatically detects CSV changes and updates frontend
 */
class DataMonitor {
    constructor(options = {}) {
        this.checkInterval = options.checkInterval || 30000; // 30 seconds
        this.autoReload = options.autoReload !== false; // Default: true
        this.isMonitoring = false;
        this.lastDataStatus = null;
        this.changeCallbacks = [];
        
        // Initialize
        this.init();
    }
    
    init() {
        // Start monitoring when page loads
        this.startMonitoring();
        
        // Set up periodic checks
        setInterval(() => {
            if (this.isMonitoring) {
                this.checkForChanges();
            }
        }, this.checkInterval);
        
        // Check for changes when page becomes visible
        document.addEventListener('visibilitychange', () => {
            if (!document.hidden && this.isMonitoring) {
                this.checkForChanges();
            }
        });
    }
    
    startMonitoring() {
        this.isMonitoring = true;
        // monitoring started
        
        // Initial check
        this.checkForChanges();
    }
    
    stopMonitoring() {
        this.isMonitoring = false;
    }
    
    async checkForChanges() {
        try {
            const response = await fetch('/dashboard/api/check-changes/');
            const data = await response.json();
            
            if (data.changes_detected) {
                this.handleChanges(data);
            }
            
        } catch (error) {
            // silent
        }
    }
    
    async handleChanges(changeData) {
        // Notify all registered callbacks
        this.changeCallbacks.forEach(callback => {
            try {
                callback(changeData);
            } catch (error) {
            }
        });
        
        // Auto-reload if enabled
        if (this.autoReload) {
            await this.reloadData();
        }
    }
    
    async reloadData() {
        try {
            // auto-reloading
            
            const response = await fetch('/dashboard/api/force-reload/', {
                method: 'POST',
                headers: {
                    'X-CSRFToken': this.getCSRFToken(),
                    'Content-Type': 'application/json',
                }
            });
            
            const result = await response.json();
            
            if (result.success) {
                // reload completed
                this.updatePageData(result);
            } else {
                // silent
            }
            
        } catch (error) {
            // silent
        }
    }
    
    updatePageData(reloadResult) {
        // Update record counts in the UI
        this.updateRecordCounts(reloadResult);
        
        // Refresh current page data
        this.refreshCurrentPage();
    }
    
    updateRecordCounts(result) {
        // Update claims count
        const claimsCountElements = document.querySelectorAll('[data-claims-count]');
        claimsCountElements.forEach(element => {
            element.textContent = result.total_claims.toLocaleString();
        });
        
        // Update claim details count
        const detailsCountElements = document.querySelectorAll('[data-details-count]');
        detailsCountElements.forEach(element => {
            element.textContent = result.total_claim_details.toLocaleString();
        });
    }
    
    refreshCurrentPage() {
        // Check current page and refresh accordingly
        const currentPath = window.location.pathname;
        
        if (currentPath.includes('/claims/')) {
            this.refreshClaimsList();
        } else if (currentPath.includes('/claim-details/')) {
            this.refreshClaimDetails();
        } else if (currentPath.includes('/analytics/')) {
            this.refreshAnalytics();
        } else if (currentPath.includes('/dashboard/')) {
            this.refreshDashboard();
        }
    }
    
    async refreshClaimsList() {
        try {
            // Trigger HTMX refresh if available
            if (window.htmx) {
                htmx.trigger('#claims-container', 'refresh');
            } else {
                // Fallback: reload the page
                window.location.reload();
            }
        } catch (error) {
            // silent
        }
    }
    
    async refreshClaimDetails() {
        try {
            if (window.htmx) {
                htmx.trigger('#claim-details-container', 'refresh');
            } else {
                window.location.reload();
            }
        } catch (error) {
            // silent
        }
    }
    
    async refreshAnalytics() {
        try {
            if (window.htmx) {
                htmx.trigger('#analytics-container', 'refresh');
            } else {
                window.location.reload();
            }
        } catch (error) {
            // silent
        }
    }
    
    async refreshDashboard() {
        try {
            if (window.htmx) {
                htmx.trigger('#dashboard-container', 'refresh');
            } else {
                window.location.reload();
            }
        } catch (error) {
            // silent
        }
    }
    
    getCSRFToken() {
        return document.querySelector('[name=csrfmiddlewaretoken]')?.value || 
               document.cookie.match(/csrftoken=([^;]+)/)?.[1] || '';
    }
    
    // Register callback for change events
    onDataChange(callback) {
        this.changeCallbacks.push(callback);
    }
    
    // Manual check for changes
    async manualCheck() {
        await this.checkForChanges();
    }
    
    // Manual reload
    async manualReload() {
        await this.reloadData();
    }
}

// Global instance
window.dataMonitor = new DataMonitor({
    checkInterval: 30000, // 30 seconds
    autoReload: true
});

// Export for module systems
if (typeof module !== 'undefined' && module.exports) {
    module.exports = DataMonitor;
}
