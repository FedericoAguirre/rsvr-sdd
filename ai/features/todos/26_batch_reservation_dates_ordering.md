# 056 — Organize Batch Reservation Modal Dates into Weekly Groups

**Status**: Ready for Implementation  
**Complexity**: 2  
**Priority**: High  
**Epic**: User Experience

---

## Objective

Reorganize the date selection display in the batch reservation modal (`/payments/{id}/?batch_modal=1`) to show 20 dates in logical weekly groups (5 dates per line, Monday-Friday), improving readability and reducing confusion when selecting dates.

---

## Motivation

**Current State**: The batch reservation modal displays 20 available dates in a single fluid line, making it difficult to:
- Visualize which dates belong to the same week
- Quickly scan dates by day of the week
- Identify patterns in available class days
- Select dates without mistakes or double-checking

**Problem**:
- All 20 dates compressed into one line causes visual overwhelm
- No indication of which day each date represents
- Users must carefully count positions to find desired dates
- Increased error rate when assigning dates to reserve
- Poor accessibility for users with vision impairments

**Desired State**:
- 20 dates organized into 4 rows of 5 dates each
- Each row represents one week (Monday through Friday)
- Clear visual grouping by week
- Day-of-week labels for clarity
- Improved scanning and selection experience

**Impact**:
- Faster, more accurate date selection
- Reduced reservation errors
- Better user satisfaction
- Improved accessibility

---

## Scope

### Changes
1. Add day-of-week labels (Lun, Mar, Mié, Jue, Vie or Mon, Tue, Wed, Thu, Fri)
2. Reorganize date display into 5-date rows
3. Add CSS grid/flexbox layout for 5-column structure
4. Add visual grouping/spacing between weeks
5. Style date buttons for improved readability
6. Ensure responsive behavior on mobile/tablet

### Out of Scope
- Change date selection logic or validation
- Modify modal header/footer
- Change payment processing flow
- Modify date availability calculation
- Add date filtering or sorting functionality (handled separately)

---

## Current Display

### Visual Problem

```
Current (Single Fluid Line):
┌─────────────────────────────────────────────────────────┐
│ 15/1  16/1  17/1  18/1  19/1  22/1  23/1  24/1  25/1   │
│ 26/1  29/1  30/1  31/1  1/2  2/2  5/2  6/2  7/2  8/2  │
└─────────────────────────────────────────────────────────┘
     Hard to scan, confusing layout, no day labels
```

**Issues**:
- Dates flow continuously without grouping
- No visual indication of weeks
- No day-of-week information
- Wrapping is automatic and unpredictable across screen sizes
- Difficult to associate dates with their weekday

---

## Desired Display

### Visual Solution

```
┌────────────────────────────────────────────────────────┐
│ Lun        Mar        Mié        Jue        Vie       │
│ ┌──────┐  ┌──────┐  ┌──────┐  ┌──────┐  ┌──────┐     │
│ │ 15/1 │  │ 16/1 │  │ 17/1 │  │ 18/1 │  │ 19/1 │     │
│ └──────┘  └──────┘  └──────┘  └──────┘  └──────┘     │
│                                                        │
│ Lun        Mar        Mié        Jue        Vie       │
│ ┌──────┐  ┌──────┐  ┌──────┐  ┌──────┐  ┌──────┐     │
│ │ 22/1 │  │ 23/1 │  │ 24/1 │  │ 25/1 │  │ 26/1 │     │
│ └──────┘  └──────┘  └──────┘  └──────┘  └──────┘     │
│                                                        │
│ Lun        Mar        Mié        Jue        Vie       │
│ ┌──────┐  ┌──────┐  ┌──────┐  ┌──────┐  ┌──────┐     │
│ │ 29/1 │  │ 30/1 │  │ 31/1 │  │  1/2 │  │  2/2 │     │
│ └──────┘  └──────┘  └──────┘  └──────┘  └──────┘     │
│                                                        │
│ Lun        Mar        Mié        Jue        Vie       │
│ ┌──────┐  ┌──────┐  ┌──────┐  ┌──────┐  ┌──────┐     │
│ │  5/2 │  │  6/2 │  │  7/2 │  │  8/2 │  │  9/2 │     │
│ └──────┘  └──────┘  └──────┘  └──────┘  └──────┘     │
│                                                        │
└────────────────────────────────────────────────────────┘
   Clear weekly grouping, labeled days, easy to scan
```

**Benefits**:
- Organized into 4 weeks of 5 dates each
- Clear day-of-week labels above each column
- Visual separation between weeks
- Predictable grid layout
- Easy to identify and select specific dates

---

## Data Structure Assumptions

The batch reservation dates are provided as a list/queryset. Assuming:

```python
# dates is a list of date objects
dates = [
    2025-01-15,  # Wed (or day_of_week value)
    2025-01-16,  # Thu
    2025-01-17,  # Fri
    # ... 17 more dates
]

# Expected: 20 dates total, representing 4 weeks of available class days
# Assumption: Dates are consecutive Monday-Friday slots (M-Tu-W-Th-Fr pattern)
```

If dates are NOT already in Monday-Friday order, the view must sort them first (see implementation).

---

## Implementation

### 1. Django View (`payments/views.py`)

Ensure dates are sorted by day of week and organized for template:

```python
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from datetime import datetime, timedelta
import calendar

def batch_reservation_modal(request, payment_id):
    """
    Fetch payment and organize available class dates for batch reservation.
    Dates are grouped into weeks of Monday-Friday.
    """
    payment = get_object_or_404(Payment, id=payment_id)
    
    # Fetch available class dates (20 dates total, Monday-Friday pattern)
    available_dates = payment.get_available_class_dates()  # Returns list of date objects
    
    # Sort dates by date value (chronological)
    available_dates = sorted(available_dates)
    
    # Organize into weeks of 5 dates each (Monday-Friday)
    weeks = []
    for i in range(0, len(available_dates), 5):
        week = available_dates[i:i+5]
        weeks.append(week)
    
    # Add day-of-week labels for each date
    week_data = []
    day_names = ['Lun', 'Mar', 'Mié', 'Jue', 'Vie']  # Spanish
    # OR: day_names = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri']  # English
    
    for week in weeks:
        week_with_labels = []
        for idx, date in enumerate(week):
            week_with_labels.append({
                'date': date,
                'day_name': day_names[idx],  # Assumes dates are in M-Tu-W-Th-Fr order
                'formatted': date.strftime('%d/%m'),  # e.g., "15/1"
                'day_of_week': calendar.day_name[date.weekday()],  # Full day name (optional)
            })
        week_data.append(week_with_labels)
    
    context = {
        'payment': payment,
        'weeks': week_data,
        'total_dates': len(available_dates),
    }
    
    return render(request, 'payments/batch_reservation_modal.html', context)


# Alternative: Handle via AJAX if modal is loaded dynamically
def batch_reservation_dates_json(request, payment_id):
    """
    Return organized weeks of dates as JSON for dynamic loading.
    """
    payment = get_object_or_404(Payment, id=payment_id)
    available_dates = sorted(payment.get_available_class_dates())
    
    weeks = []
    day_names = ['Lun', 'Mar', 'Mié', 'Jue', 'Vie']
    
    for i in range(0, len(available_dates), 5):
        week = []
        for idx, date in enumerate(available_dates[i:i+5]):
            week.append({
                'date': date.isoformat(),
                'day_name': day_names[idx],
                'formatted': date.strftime('%d/%m'),
            })
        weeks.append(week)
    
    return JsonResponse({'weeks': weeks})
```

### 2. Update Modal Template (`templates/payments/batch_reservation_modal.html`)

```html
{% extends "base.html" %}
{% load i18n %}

{% block title %}{% translate "Batch Reservation" %} - {{ payment }}{% endblock %}

{% block content %}
<div class="modal fade" id="batchReservationModal" tabindex="-1" aria-hidden="true">
    <div class="modal-dialog modal-lg modal-dialog-scrollable">
        <div class="modal-content">
            
            <!-- Modal Header -->
            <div class="modal-header">
                <h5 class="modal-title">
                    {% translate "Batch Reservation" %} - {{ payment.client.name }}
                </h5>
                <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="{% translate 'Close' %}"></button>
            </div>
            
            <!-- Modal Body -->
            <div class="modal-body">
                <form method="post" action="{% url 'payments:batch_reservation' payment.id %}" class="batch-reservation-form">
                    {% csrf_token %}
                    
                    <!-- Instructions -->
                    <p class="text-muted small">
                        {% translate "Select up to" %} {{ total_dates }} {% translate "available class dates." %}
                        {% translate "Dates are organized by week (Monday through Friday)." %}
                    </p>
                    
                    <!-- Dates Grid -->
                    <div class="batch-dates-container">
                        {% for week in weeks %}
                        <!-- Week Group -->
                        <div class="week-group">
                            <!-- Day Headers -->
                            <div class="week-header">
                                <div class="day-label">Lun</div>
                                <div class="day-label">Mar</div>
                                <div class="day-label">Mié</div>
                                <div class="day-label">Jue</div>
                                <div class="day-label">Vie</div>
                            </div>
                            
                            <!-- Date Buttons -->
                            <div class="week-dates">
                                {% for day_data in week %}
                                <div class="date-wrapper">
                                    <button 
                                        type="button" 
                                        class="date-button btn btn-outline-primary"
                                        data-date="{{ day_data.date }}"
                                        data-toggle="date-selection"
                                        title="{{ day_data.day_of_week }}, {{ day_data.date }}">
                                        {{ day_data.formatted }}
                                    </button>
                                    <!-- Hidden checkbox for form submission -->
                                    <input 
                                        type="checkbox" 
                                        name="selected_dates" 
                                        value="{{ day_data.date }}"
                                        class="date-checkbox d-none"
                                        data-date="{{ day_data.date }}">
                                </div>
                                {% endfor %}
                            </div>
                            
                            <!-- Week Separator -->
                            {% if not forloop.last %}
                            <div class="week-separator"></div>
                            {% endif %}
                        </div>
                        {% endfor %}
                    </div>
                    
                    <!-- Selection Summary -->
                    <div class="selection-summary mt-3 p-3 bg-light rounded">
                        <small>
                            <strong>{% translate "Selected:" %}</strong>
                            <span id="selected-count">0</span> / {{ total_dates }}
                            {% translate "dates" %}
                        </small>
                        <div id="selected-list" class="selected-dates-list mt-2 small"></div>
                    </div>
                </form>
            </div>
            
            <!-- Modal Footer -->
            <div class="modal-footer">
                <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">
                    {% translate "Cancel" %}
                </button>
                <button type="button" class="btn btn-primary" id="confirm-batch-reservation">
                    {% translate "Create Reservations" %}
                </button>
            </div>
        </div>
    </div>
</div>

<style>
    /* Batch Reservation Modal Styling */
    
    /* Main container for dates grid */
    .batch-dates-container {
        max-height: 400px;
        overflow-y: auto;
        padding: 1rem;
        background-color: #f8f9fa;
        border-radius: 0.375rem;
    }
    
    /* Week Group */
    .week-group {
        margin-bottom: 1rem;
        padding: 0.75rem;
        background-color: white;
        border-radius: 0.375rem;
        border-left: 3px solid #0d6efd;
    }
    
    /* Day Header Row */
    .week-header {
        display: grid;
        grid-template-columns: repeat(5, 1fr);
        gap: 0.5rem;
        margin-bottom: 0.75rem;
        padding-bottom: 0.75rem;
        border-bottom: 2px solid #e9ecef;
    }
    
    /* Day Label (Mon, Tue, etc.) */
    .day-label {
        text-align: center;
        font-weight: 600;
        font-size: 0.85rem;
        color: #6c757d;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    /* Week Dates Row */
    .week-dates {
        display: grid;
        grid-template-columns: repeat(5, 1fr);
        gap: 0.5rem;
    }
    
    /* Date Wrapper (for proper alignment) */
    .date-wrapper {
        display: flex;
        align-items: center;
        justify-content: center;
    }
    
    /* Date Button */
    .date-button {
        width: 100%;
        padding: 0.5rem 0.25rem;
        font-size: 0.9rem;
        font-weight: 500;
        border: 2px solid #dee2e6;
        border-radius: 0.375rem;
        cursor: pointer;
        transition: all 0.2s ease;
        background-color: white;
        color: #495057;
    }
    
    .date-button:hover {
        border-color: #0d6efd;
        color: #0d6efd;
        background-color: #f0f6ff;
        transform: translateY(-2px);
    }
    
    /* Active/Selected State */
    .date-button.active {
        background-color: #0d6efd;
        color: white;
        border-color: #0d6efd;
        box-shadow: 0 0 0 3px rgba(13, 110, 253, 0.25);
    }
    
    .date-button.active:hover {
        background-color: #0b5ed7;
        border-color: #0b5ed7;
    }
    
    /* Week Separator */
    .week-separator {
        height: 1px;
        background-color: #e9ecef;
        margin: 0.75rem 0;
        opacity: 0.5;
    }
    
    /* Selection Summary */
    .selection-summary {
        border-left: 3px solid #198754;
    }
    
    .selected-dates-list {
        display: flex;
        flex-wrap: wrap;
        gap: 0.5rem;
    }
    
    .selected-date-badge {
        display: inline-block;
        background-color: #0d6efd;
        color: white;
        padding: 0.25rem 0.5rem;
        border-radius: 0.25rem;
        font-size: 0.8rem;
    }
    
    /* Responsive Adjustments */
    @media (max-width: 768px) {
        .batch-dates-container {
            max-height: 300px;
            padding: 0.5rem;
        }
        
        .week-group {
            padding: 0.5rem;
            margin-bottom: 0.75rem;
        }
        
        .week-header {
            gap: 0.25rem;
            margin-bottom: 0.5rem;
            padding-bottom: 0.5rem;
        }
        
        .day-label {
            font-size: 0.75rem;
        }
        
        .week-dates {
            gap: 0.25rem;
        }
        
        .date-button {
            padding: 0.375rem 0.125rem;
            font-size: 0.8rem;
        }
    }
    
    /* Print Styles */
    @media print {
        .batch-dates-container {
            max-height: none;
            overflow: visible;
        }
    }
</style>

<!-- Date Selection JavaScript -->
<script>
    document.addEventListener('DOMContentLoaded', function() {
        // Cache DOM elements
        const dateButtons = document.querySelectorAll('.date-button');
        const dateCheckboxes = document.querySelectorAll('.date-checkbox');
        const selectedCountSpan = document.getElementById('selected-count');
        const selectedListDiv = document.getElementById('selected-list');
        const confirmButton = document.getElementById('confirm-batch-reservation');
        
        // Track selected dates
        const selectedDates = new Set();
        
        // Handle date button clicks
        dateButtons.forEach(button => {
            button.addEventListener('click', function(e) {
                e.preventDefault();
                
                const dateValue = this.dataset.date;
                const checkbox = document.querySelector(`input[data-date="${dateValue}"]`);
                
                // Toggle selection
                if (selectedDates.has(dateValue)) {
                    selectedDates.delete(dateValue);
                    this.classList.remove('active');
                    checkbox.checked = false;
                } else {
                    selectedDates.add(dateValue);
                    this.classList.add('active');
                    checkbox.checked = true;
                }
                
                // Update summary
                updateSelectionSummary();
            });
        });
        
        // Update selection summary display
        function updateSelectionSummary() {
            const count = selectedDates.size;
            selectedCountSpan.textContent = count;
            
            // Build selected dates list
            const selectedList = Array.from(selectedDates).sort();
            selectedListDiv.innerHTML = selectedList.map(date => {
                return `<span class="selected-date-badge">${formatDateForDisplay(date)}</span>`;
            }).join('');
            
            // Enable/disable confirm button
            confirmButton.disabled = count === 0;
        }
        
        // Format date for display (adjust format as needed)
        function formatDateForDisplay(dateString) {
            const date = new Date(dateString);
            return date.toLocaleDateString('es-ES', { 
                year: 'numeric', 
                month: '2-digit', 
                day: '2-digit' 
            });
        }
        
        // Handle confirm button
        confirmButton.addEventListener('click', function() {
            if (selectedDates.size > 0) {
                // Submit form with selected dates
                const form = document.querySelector('.batch-reservation-form');
                form.submit();
            }
        });
        
        // Disable confirm button initially
        confirmButton.disabled = true;
    });
</script>
{% endblock %}
```

### 3. URL Configuration (`payments/urls.py`)

Add routes for batch reservation modal:

```python
from django.urls import path
from . import views

app_name = 'payments'

urlpatterns = [
    # ... existing URLs ...
    
    # Batch reservation modal
    path(
        '<int:payment_id>/batch-modal/',
        views.batch_reservation_modal,
        name='batch_modal'
    ),
    
    # Alternative: AJAX endpoint for fetching dates
    path(
        '<int:payment_id>/batch-dates-json/',
        views.batch_reservation_dates_json,
        name='batch_dates_json'
    ),
    
    # Handle batch reservation form submission
    path(
        '<int:payment_id>/batch-reservation/',
        views.create_batch_reservations,
        name='batch_reservation'
    ),
]
```

---

## Layout Grid

### CSS Grid Structure

The grid uses 5 columns (one per weekday):

```css
.week-dates {
    display: grid;
    grid-template-columns: repeat(5, 1fr);  /* 5 equal columns */
    gap: 0.5rem;  /* Spacing between date buttons */
}
```

This ensures:
- Exactly 5 dates per row
- Equal column widths
- Consistent alignment
- Responsive scaling on smaller screens

### Visual Alignment

```
┌─────────┬─────────┬─────────┬─────────┬─────────┐
│   Lun   │   Mar   │   Mié   │   Jue   │   Vie   │  Header
├─────────┼─────────┼─────────┼─────────┼─────────┤
│ [15/1]  │ [16/1]  │ [17/1]  │ [18/1]  │ [19/1]  │  Week 1
├─────────┼─────────┼─────────┼─────────┼─────────┤
│ [22/1]  │ [23/1]  │ [24/1]  │ [25/1]  │ [26/1]  │  Week 2
├─────────┼─────────┼─────────┼─────────┼─────────┤
│ [29/1]  │ [30/1]  │ [31/1]  │ [ 1/2]  │ [ 2/2]  │  Week 3
├─────────┼─────────┼─────────┼─────────┼─────────┤
│ [ 5/2]  │ [ 6/2]  │ [ 7/2]  │ [ 8/2]  │ [ 9/2]  │  Week 4
└─────────┴─────────┴─────────┴─────────┴─────────┘
```

---

## Interaction Behavior

### Date Selection
- Click date button to select/deselect
- Selected dates show visual feedback (blue background, white text)
- Multiple selections allowed
- Selection count updates in real-time

### Visual Feedback
1. **Hover State**: Button border changes to primary color, slight lift effect
2. **Active State**: Button filled with primary color, white text
3. **Selection Summary**: Shows number of selected dates and list of selections

### Form Submission
- Hidden checkboxes store selected dates for form submission
- Confirm button disabled until at least one date is selected
- Form submits selected dates to backend for processing

---

## Testing Checklist

### Layout & Display
- [ ] Exactly 5 dates appear per row (no wrapping within rows)
- [ ] 4 weeks total (20 dates ÷ 5 per row)
- [ ] Day-of-week labels visible above each column
- [ ] Visual separation between weeks is clear
- [ ] Week labels maintain alignment across all weeks
- [ ] Modal scrolls vertically without horizontal scrolling
- [ ] All dates fully visible and readable

### Interactions
- [ ] Clicking date button toggles selection state
- [ ] Selected button shows active styling (blue background)
- [ ] Deselected button returns to outline styling
- [ ] Selection count updates in real-time
- [ ] Selected dates list updates as selections change
- [ ] Confirm button is disabled when no dates selected
- [ ] Confirm button is enabled when dates selected

### Responsiveness
- [ ] Desktop (> 1024px): Full grid layout
- [ ] Tablet (768px - 1024px): Grid remains 5 columns, may need scrolling
- [ ] Mobile (< 768px): Grid adjusts or stacks (with consideration for usability)
- [ ] No horizontal scrolling on any device
- [ ] Dates remain clickable on all screen sizes

### Accessibility
- [ ] All date buttons have proper ARIA labels
- [ ] Selection count is announced to screen readers
- [ ] Keyboard navigation works (Tab, Enter)
- [ ] Focus states are visible
- [ ] Color is not the only indicator of selection (shape/text changes too)
- [ ] Help text "dates organized by week" is clear

### Functional
- [ ] Form submission includes selected dates
- [ ] Backend receives correct date values
- [ ] Reservations created for all selected dates
- [ ] No duplicate reservations created
- [ ] Error handling displays properly
- [ ] Success message appears after creation

### Cross-Browser
- [ ] Chrome/Chromium 90+
- [ ] Firefox 88+
- [ ] Safari 14+
- [ ] Edge 90+
- [ ] Mobile Chrome
- [ ] Mobile Safari

---

## Data Assumptions

**Input**: List of 20 available class dates (in chronological order)

**Expected Format**:
- Dates are sorted chronologically
- Dates represent consecutive Monday-Friday class slots
- No gaps or missing days within weeks
- Format: Python `date` objects or ISO 8601 strings

**Processing**:
1. Sort dates chronologically
2. Group into sets of 5 (Monday-Friday)
3. Generate day-of-week labels based on position in group
4. Pass to template as nested list: `[[week1_dates], [week2_dates], ...]`

**Validation**:
- Dates must be valid date objects
- Must have exactly 20 dates (4 weeks × 5 days)
- Dates should represent weekdays only (no weekends)

---

## Success Criteria

- ✅ All 20 dates display in 5-date rows (4 total rows)
- ✅ Clear day-of-week labels above each column
- ✅ Logical visual grouping by week
- ✅ No dates wrap unexpectedly
- ✅ Selection interaction works smoothly
- ✅ Real-time feedback on selections
- ✅ Responsive on all device sizes
- ✅ Accessible to screen readers
- ✅ Form submission includes selected dates
- ✅ Modal fits within standard viewport heights

---

## Optional Enhancements (Future)

These are not part of this spec but could be added later:

1. **Week Numbers**: Display week numbers (W1, W2, etc.)
2. **Select All/None**: Buttons to select/deselect entire weeks
3. **Color Coding**: Different colors for different time slots or class types
4. **Tooltips**: Show class time or class name on hover
5. **Keyboard Shortcuts**: Use arrow keys to navigate dates
6. **Date Range Selection**: Shift+click to select date ranges
7. **Export**: Export selected dates to calendar or spreadsheet

---

## Deliverables

1. Updated `payments/views.py` with date organization logic
2. New/Updated template: `templates/payments/batch_reservation_modal.html`
3. CSS styling for grid layout and date buttons
4. JavaScript for date selection interactivity
5. Updated URL configuration in `payments/urls.py`
6. Testing report confirming all checklist items

---

## Timeline

- **Implementation**: ~1 hour (view logic + template + styling)
- **Testing**: ~1 hour (layout, interaction, responsiveness)
- **Refinement**: ~30 minutes (CSS tweaks, accessibility)

**Total**: ~2.5 hours

---

## References

- [CSS Grid Layout](https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_Grid_Layout)
- [Bootstrap Modal Documentation](https://getbootstrap.com/docs/5.3/components/modal/)
- [Date Handling in Django](https://docs.djangoproject.com/en/5.0/topics/i18n/timezones/)
- [Python calendar Module](https://docs.python.org/3/library/calendar.html)
- [Accessibility Guidelines for Date Pickers](https://www.w3.org/WAI/tutorials/forms/multi-page/)
