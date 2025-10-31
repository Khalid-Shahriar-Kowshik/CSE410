from django.shortcuts import render,redirect, get_object_or_404
from .models import CPU,MOBO,CPUCooler,RAM,Storage,GPU,PSU,CASE
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import CartItem, Order, OrderItem
from django.db.models import Sum, F
from collections import defaultdict
import re

@login_required
def order_list(request):
    orders = request.user.orders.all()
    return render(request, "order_list.html", {"orders": orders})

@login_required
def add_to_cart(request, product_type, product_id):
    product_model = {
        "CPU": CPU,
        "GPU": GPU,
        "RAM": RAM,
        "Storage": Storage,
        "PSU": PSU,
        "CASE": CASE,
        "MOBO": MOBO,
        "CPUCooler": CPUCooler,
    }.get(product_type)

    if not product_model:
        messages.error(request, "Invalid product type!")
        return redirect("home")

    product = get_object_or_404(product_model, id=product_id)
    cart_item, created = CartItem.objects.get_or_create(
        user=request.user,
        product_type=product_type,
        product_id=product_id,
        defaults={"price": product.price, "quantity": 1},
    )
    if not created:
        cart_item.quantity += 1
        cart_item.save()

    messages.success(request, f"{product.name} added to your cart.")
    return redirect(product_type.lower())


@login_required
def view_cart(request):
    cart_items = CartItem.objects.filter(user=request.user)
    total_amount = sum(item.total_price for item in cart_items)
    return render(request, "cart.html", {"cart_items": cart_items, "total_amount": total_amount})

@login_required
def remove_from_cart(request, cart_item_id):
    cart_item = get_object_or_404(CartItem, id=cart_item_id, user=request.user)
    cart_item.delete()
    messages.success(request, "Item removed from cart.")
    return redirect("cart_view")

@login_required
def place_order(request):
    cart_items = CartItem.objects.filter(user=request.user)
    if not cart_items:
        messages.error(request, "Your cart is empty!")
        return redirect("cart_view")

    total_amount = sum(item.total_price for item in cart_items)
    order = Order.objects.create(user=request.user, total_amount=total_amount)

    for item in cart_items:
        product = item.product_object
        OrderItem.objects.create(
            order=order,
            product_type=item.product_type,
            product_id=item.product_id,
            quantity=item.quantity,
            price=item.price,
        )

    messages.success(request, f"Build #{order.id} saved successfully! You can continue adding more items.")
    return redirect("cart_view")


@login_required
def delete_order(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)

    if request.method == 'POST':
        order.delete()
        messages.success(request, "Build deleted successfully!")
        return redirect('order_list')

    messages.error(request, "Invalid request method")
    return redirect('order_list')


@login_required
def order_details(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)

    items_with_products = []
    for item in order.items.all():
        product = None
        model_map = {
            'CPU': CPU,
            'MOBO': MOBO,
            'CPUCooler': CPUCooler,
            'RAM': RAM,
            'Storage': Storage,
            'GPU': GPU,
            'PSU': PSU,
            'CASE': CASE,
        }
        model = model_map.get(item.product_type)
        if model:
            product = model.objects.filter(id=item.product_id).first()

        items_with_products.append({
            'item': item,
            'product': product
        })

    return render(request, "order_details.html", {
        "order": order,
        "items_with_products": items_with_products
    })

def cpu(request):
    cpu= CPU.objects.all()
    return render(request,'products/cpu.html',{'cpu':cpu})

def mobo(request):
    mobo= MOBO.objects.all()
    return render(request,'products/mobo.html',{'mobo':mobo})

def cpucooler(request):
    cpucooler= CPUCooler.objects.all()
    return render(request,'products/cpucooler.html',{'cpucooler':cpucooler})

def ram(request):
    ram= RAM.objects.all()
    return render(request,'products/ram.html',{'ram':ram})

def storage(request):
    storage= Storage.objects.all()
    return render(request,'products/storage.html',{'storage':storage})

def gpu(request):
    gpu= GPU.objects.all()
    return render(request,'products/gpu.html',{'gpu':gpu})

def case(request):
    case= CASE.objects.all()
    return render(request,'products/case.html',{'case':case})

def psu(request):
    psu= PSU.objects.all()
    return render(request,'products/psu.html',{'psu':psu})


def cpu_detail(request, cpu_id):
    cpu = get_object_or_404(CPU, id=cpu_id)
    return render(request, 'products/details.html', {'object': cpu})

def mobo_detail(request, mobo_id):
    mobo = get_object_or_404(MOBO, id=mobo_id)
    return render(request, 'products/details.html', {'object': mobo})

def cpu_cooler_detail(request, cooler_id):
    cooler = get_object_or_404(CPUCooler, id=cooler_id)
    return render(request, 'products/details.html', {'object': cooler})

def ram_detail(request, ram_id):
    ram = get_object_or_404(RAM, id=ram_id)
    return render(request, 'products/details.html', {'object': ram})

def storage_detail(request, storage_id):
    storage = get_object_or_404(Storage, id=storage_id)
    return render(request, 'products/details.html', {'object': storage})

def gpu_detail(request, gpu_id):
    gpu = get_object_or_404(GPU, id=gpu_id)
    return render(request, 'products/details.html', {'object': gpu})

def psu_detail(request, psu_id):
    psu = get_object_or_404(PSU, id=psu_id)
    return render(request, 'products/details.html', {'object': psu})

def case_detail(request, case_id):
    case = get_object_or_404(CASE, id=case_id)
    return render(request, 'products/details.html', {'object': case})

# Product search and autocomplete
def product_search(request):
    q = request.GET.get('q', '').strip()
    results = []
    if q:
        # search each product model by name (case-insensitive)
        cpus = CPU.objects.filter(name__icontains=q)
        mobos = MOBO.objects.filter(name__icontains=q)
        coolers = CPUCooler.objects.filter(name__icontains=q)
        rams = RAM.objects.filter(name__icontains=q)
        storages = Storage.objects.filter(name__icontains=q)
        gpus = GPU.objects.filter(name__icontains=q)
        psus = PSU.objects.filter(name__icontains=q)
        cases = CASE.objects.filter(name__icontains=q)

        # add tuples of (object, type_name, detail_url_name)
        for o in cpus: results.append((o, 'CPU', 'cpu_detail'))
        for o in mobos: results.append((o, 'MOBO', 'mobo_detail'))
        for o in coolers: results.append((o, 'CPU Cooler', 'cpu_cooler_detail'))
        for o in rams: results.append((o, 'RAM', 'ram_detail'))
        for o in storages: results.append((o, 'Storage', 'storage_detail'))
        for o in gpus: results.append((o, 'GPU', 'gpu_detail'))
        for o in psus: results.append((o, 'PSU', 'psu_detail'))
        for o in cases: results.append((o, 'Case', 'case_detail'))

    return render(request, 'products/search_results.html', {
        'query': q,
        'results': results,
    })


from django.http import JsonResponse
from django.urls import reverse
from django.templatetags.static import static as static_url

def product_autocomplete(request):
    q = request.GET.get('q', '').strip()
    suggestions = []
    if q:
        # search name and return limited suggestions
        limit = 8
        models = [
            (CPU, 'CPU', 'cpu_detail'),
            (MOBO, 'MOBO', 'mobo_detail'),
            (CPUCooler, 'CPU Cooler', 'cpu_cooler_detail'),
            (RAM, 'RAM', 'ram_detail'),
            (Storage, 'Storage', 'storage_detail'),
            (GPU, 'GPU', 'gpu_detail'),
            (PSU, 'PSU', 'psu_detail'),
            (CASE, 'Case', 'case_detail'),
        ]

        for model, type_name, url_name in models:
            qs = model.objects.filter(name__icontains=q)[:limit]
            for o in qs:
                # determine thumbnail: model.photo if present, else fallback static image
                thumb = ''
                try:
                    if getattr(o, 'photo', None) and getattr(o, 'photo').url:
                        thumb = o.photo.url
                except Exception:
                    thumb = ''
                if not thumb:
                    thumb = static_url('image/logo.png')

                # convert relative media/static URLs to absolute URLs so clients can load them
                try:
                    thumb = request.build_absolute_uri(thumb)
                except Exception:
                    # fallback to the value as-is if build_absolute_uri fails for any reason
                    pass

                # build absolute URL for detail page
                try:
                    detail_url = request.build_absolute_uri(reverse(url_name, args=[o.id]))
                except Exception:
                    detail_url = reverse(url_name, args=[o.id])

                suggestions.append({
                    'id': o.id,
                    'name': o.name,
                    'type': type_name,
                    'price': getattr(o, 'price', ''),
                    'url': detail_url,
                    'thumbnail': thumb,
                })
                if len(suggestions) >= limit:
                    break
            if len(suggestions) >= limit:
                break

    return JsonResponse({'results': suggestions})


@login_required
def view_cart(request):
    cart_items = CartItem.objects.filter(user=request.user)
    components = {
        'CPU': None,
        'MOBO': None,
        'RAM': [],
        'PSU': None,
        'CASE': None,
        'CPUCooler': None,
        'Storage': [],
        'GPU': None,
    }
    compatibility_issues = defaultdict(list)

    for item in cart_items:
        prod = item.product_object
        if not prod:
            continue
        if item.product_type in ['RAM', 'Storage']:
            components[item.product_type].append(prod)
        else:
            components[item.product_type] = prod

    cpu = components['CPU']; mobo = components['MOBO']; psu = components['PSU']
    case = components['CASE']; cooler = components['CPUCooler']; rams = components['RAM']
    gpu = components['GPU']; storages = components['Storage']

    def flag(ptype, pid, msg):
        '''Attach a compatibility message to all cart_items matching product type & id.'''
        for it in cart_items.filter(product_type=ptype, product_id=pid):
            compatibility_issues[it.id].append(msg)

    def norm(val): return val.strip().lower() if isinstance(val, str) else val
    def split_multi(val):
        if not isinstance(val, str):
            return []
        parts = re.split(r'[\\/,\s]+', val)
        return [norm(p) for p in parts if p]

    # 1. CPU <-> Motherboard socket/platform
    if cpu and mobo:
        mobo_platforms = split_multi(mobo.platform)
        if norm(cpu.platform) not in mobo_platforms:
            msg = f"CPU socket ({cpu.platform}) doesn't match Motherboard ({mobo.platform})"
            flag('CPU', cpu.id, msg); flag('MOBO', mobo.id, msg)

    # 2. RAM <-> Motherboard type & capacity
    if mobo and rams:
        total_ram = sum(r.ram_capacity for r in rams)
        mobo_ram_types = split_multi(mobo.ram_type)
        for ram in rams:
            if norm(ram.ram_type) not in mobo_ram_types:
                msg = f"RAM type ({ram.ram_type}) not supported by motherboard ({mobo.ram_type})"
                flag('RAM', ram.id, msg)
        if total_ram > mobo.ram_capacity:
            msg = f"Total RAM ({total_ram}GB) exceeds motherboard max ({mobo.ram_capacity}GB)"
            for ram in rams: flag('RAM', ram.id, msg)

    # 3. Storage <-> M.2 slots
    if mobo and storages:
        nvme_count = sum(1 for s in storages if norm(s.interface) == 'nvme')
        if hasattr(mobo, 'm2_slots') and nvme_count > mobo.m2_slots:
            msg = f"NVMe drives ({nvme_count}) exceed motherboard M.2 slots ({mobo.m2_slots})"
            for s in storages: flag('Storage', s.id, msg)

    # 4. PSU power budgeting
    total_power = sum([
        cpu.power if cpu else 0,
        mobo.power if mobo else 0,
        sum(r.power for r in rams),
        sum(s.power for s in storages),
        gpu.power if gpu else 0,
    ])
    if psu and psu.capacity < total_power:
        msg = f"PSU capacity ({psu.capacity}W) insufficient for estimated draw ({total_power}W)"
        flag('PSU', psu.id, msg)

    # # 5. Case <-> Motherboard form factor
    # if case and mobo and hasattr(case, 'mobo_form_factor'):
    #     supported = split_multi(case.mobo_form_factor)
    #     if norm(mobo.mobo_form_factor) not in supported:
    #         msg = f"Case doesn't support {mobo.mobo_form_factor} motherboards"
    #         flag('CASE', case.id, msg)

    # 6. GPU <-> Case clearance
    if case and gpu and hasattr(case, 'gpu_and_cooler_clearance') and hasattr(gpu, 'dimension_weight'):
        try:
            #extract GPU length from string like "357.6 x 149.3 x 70.1mm"
            gpu_dimensions = gpu.dimension_weight.lower().replace('mm', '').strip()
            gpu_length_str = gpu_dimensions.split('x')[0].strip()
            gpu_length = float(gpu_length_str)

            #extract Case GPU clearance from string like "350mm,160mm"
            clearance_parts = case.gpu_and_cooler_clearance.lower().replace('mm', '').split(',')
            case_gpu_clearance = float(clearance_parts[0].strip())

            if gpu_length > case_gpu_clearance:
                msg = f"GPU length ({gpu_length}mm) exceeds case max clearance ({case_gpu_clearance}mm)"
                flag('GPU', gpu.id, msg)
                flag('CASE', case.id, msg)
        except Exception as e:
            print(f"Compatibility check failed: {e}")

    # 7. Cooler <-> Case height & CPU socket
    if cooler and cpu:
        sup = split_multi(cooler.platform)
        if norm(cpu.platform) not in sup:
            msg = f"Cooler not compatible with {cpu.platform} socket"
            flag('CPUCooler', cooler.id, msg)
        if case and hasattr(case, 'max_cooler_height') and hasattr(cooler, 'height'):
            if cooler.height > case.max_cooler_height:
                msg = f"Cooler height ({cooler.height}mm) exceeds case limit ({case.max_cooler_height}mm)"
                flag('CPUCooler', cooler.id, msg); flag('CASE', case.id, msg)

    # # 8. PSU size <-> Case PSU bay
    # if psu and case and hasattr(psu, 'length') and hasattr(case, 'max_psu_length'):
    #     if psu.length > case.max_psu_length:
    #         msg = f"PSU length ({psu.length}mm) exceeds case PSU bay limit ({case.max_psu_length}mm)"
    #         flag('PSU', psu.id, msg); flag('CASE', case.id, msg)

    # 9. liquid Cooler radiator <-> Case fan
    #coming soon once the model fields are more organized

    # Calculate total
    total_amount = sum(item.total_price for item in cart_items)
    return render(request, 'cart.html', {
        'cart_items': cart_items,
        'total_amount': total_amount,
        'compatibility_issues': dict(compatibility_issues),
    })


def cpu(request):
    sort_by = request.GET.get('sort', 'default')
    cpus = CPU.objects.all()

    if sort_by == 'price_low':
        cpus = cpus.order_by('price')
    elif sort_by == 'price_high':
        cpus = cpus.order_by('-price')
    elif sort_by == 'name_asc':
        cpus = cpus.order_by('name')
    elif sort_by == 'name_desc':
        cpus = cpus.order_by('-name')

    return render(request, 'products/cpu.html', {
        'cpu': cpus,
        'current_sort': sort_by
    })


def mobo(request):
    sort_by = request.GET.get('sort', 'default')
    mobos = MOBO.objects.all()

    if sort_by == 'price_low':
        mobos = mobos.order_by('price')
    elif sort_by == 'price_high':
        mobos = mobos.order_by('-price')
    elif sort_by == 'name_asc':
        mobos = mobos.order_by('name')
    elif sort_by == 'name_desc':
        mobos = mobos.order_by('-name')

    return render(request, 'products/mobo.html', {
        'mobo': mobos,
        'current_sort': sort_by
    })


def cpucooler(request):
    sort_by = request.GET.get('sort', 'default')
    coolers = CPUCooler.objects.all()

    if sort_by == 'price_low':
        coolers = coolers.order_by('price')
    elif sort_by == 'price_high':
        coolers = coolers.order_by('-price')
    elif sort_by == 'name_asc':
        coolers = coolers.order_by('name')
    elif sort_by == 'name_desc':
        coolers = coolers.order_by('-name')

    return render(request, 'products/cpucooler.html', {
        'cpucooler': coolers,
        'current_sort': sort_by
    })


def ram(request):
    sort_by = request.GET.get('sort', 'default')
    rams = RAM.objects.all()

    if sort_by == 'price_low':
        rams = rams.order_by('price')
    elif sort_by == 'price_high':
        rams = rams.order_by('-price')
    elif sort_by == 'name_asc':
        rams = rams.order_by('name')
    elif sort_by == 'name_desc':
        rams = rams.order_by('-name')

    return render(request, 'products/ram.html', {
        'ram': rams,
        'current_sort': sort_by
    })


def storage(request):
    sort_by = request.GET.get('sort', 'default')
    storages = Storage.objects.all()

    if sort_by == 'price_low':
        storages = storages.order_by('price')
    elif sort_by == 'price_high':
        storages = storages.order_by('-price')
    elif sort_by == 'name_asc':
        storages = storages.order_by('name')
    elif sort_by == 'name_desc':
        storages = storages.order_by('-name')

    return render(request, 'products/storage.html', {
        'storage': storages,
        'current_sort': sort_by
    })


def gpu(request):
    sort_by = request.GET.get('sort', 'default')
    gpus = GPU.objects.all()

    if sort_by == 'price_low':
        gpus = gpus.order_by('price')
    elif sort_by == 'price_high':
        gpus = gpus.order_by('-price')
    elif sort_by == 'name_asc':
        gpus = gpus.order_by('name')
    elif sort_by == 'name_desc':
        gpus = gpus.order_by('-name')

    return render(request, 'products/gpu.html', {
        'gpu': gpus,
        'current_sort': sort_by
    })


def case(request):
    sort_by = request.GET.get('sort', 'default')
    cases = CASE.objects.all()

    if sort_by == 'price_low':
        cases = cases.order_by('price')
    elif sort_by == 'price_high':
        cases = cases.order_by('-price')
    elif sort_by == 'name_asc':
        cases = cases.order_by('name')
    elif sort_by == 'name_desc':
        cases = cases.order_by('-name')

    return render(request, 'products/case.html', {
        'case': cases,
        'current_sort': sort_by
    })


def psu(request):
    sort_by = request.GET.get('sort', 'default')
    psus = PSU.objects.all()

    if sort_by == 'price_low':
        psus = psus.order_by('price')
    elif sort_by == 'price_high':
        psus = psus.order_by('-price')
    elif sort_by == 'name_asc':
        psus = psus.order_by('name')
    elif sort_by == 'name_desc':
        psus = psus.order_by('-name')

    return render(request, 'products/psu.html', {
        'psu': psus,
        'current_sort': sort_by
    })