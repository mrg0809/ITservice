import datetime
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Ticket
from .form import CreateTicketForm, UpdateTicketForm

# view ticket details
def ticket_details(request, pk):
    ticket = Ticket.objects.get(pk=pk)
    context = {'ticket':ticket}
    return render(request, 'ticket/ticket_detail.html', context)

'''For customers'''
# Create a ticket
def create_ticket(request):
    if request.method == 'POST':
        form = CreateTicketForm(request.POST)
        if form.is_valid():
            var = form.save(commit=False)
            var.created_by = request.user
            var.ticket_status = 'Pending'
            var.save()
            messages.info(request, 'Your ticket has been successfully submitted. An engineer would be asigned soon')
            return redirect('dashboard')
        else:
            messages.warning(request, 'Something were wrong, Please check form input')
            return redirect('create-ticket')
    else:
        form = CreateTicketForm()
        context = {'form':form}
        return render(request, 'ticket/create_ticket.html', context)
    
# Update ticket
def update_ticket(request, pk):
    ticket = Ticket.objects.get(pk=pk)
    if request.method == 'POST':
        form = UpdateTicketForm(request.POST, instance=ticket)
        if form.is_valid():
            form.save()            
            messages.info(request, 'Your ticket info has been updated.')
            #return redirect('dashboard')
        else:
            messages.warning(request, 'Something were wrong, Please check form input')
            return redirect('create-ticket')
    else:
        form = UpdateTicketForm(instance=ticket)
        context = {'form':form}
        return render(request, 'ticket/update_ticket.html', context)
    
#View all tickets
def all_tickets(request):
    tickets = Ticket.objects.filter(created_by=request.user)
    context = {'tickets':tickets}
    return render(request, 'ticket/all_tickets.html', context)


'''For engineers'''

# View tickets queue
def ticket_queue(request):
    tickets = Ticket.objects.filter(ticket_status='Pending')
    context = {'tickets':tickets}
    return render(request, 'ticket/ticket_queue.html', context)

# Accept ticket
def accept_ticket(request, pk):
    ticket = Ticket.objects.get(pk=pk)
    ticket.assigned_to = request.user
    ticket.ticket_status = 'Active'
    ticket.accepted_date = datetime.datetime.now()
    ticket.save()
    messages.info(request, 'Ticket has been accepted. Please resolve as soon as posible')
    return redirect('tickets-queue')

# Close ticket
def close_ticket(request, pk):
    ticket = Ticket.objects.get(pk=pk)
    ticket.ticket_status = 'Completed'
    ticket.is_resolved = True
    ticket.closed_date = datetime.datetime.now()
    ticket.save()
    messages.info(request, 'Ticket has been resolved.')
    return redirect('tickets-queue')

# Tickets working on
def workspace(request):
    tickets = Ticket.objects.filter(assigned_to=request.user, is_resolved=False)
    context = {'tickets':tickets}
    return render(request, 'ticket/workspace.html', context)

# Vies all closed/resolved tickets
def all_closed_tickets(request):
    tickets = Ticket.objects.filter(assigned_to=request.user, is_resolved=True)
    context = {'tickets':tickets}
    return render(request, 'ticket/all_closed_tickets.html', context)

